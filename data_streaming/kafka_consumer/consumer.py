import sys

import psycopg2
import pyspark
from config import configs
from load_schedules import process_schedules_stream
from pyspark.sql import SparkSession
from pyspark.sql.streaming import DataStreamWriter


def _create_spark_session() -> pyspark.sql.SparkSession:
    """
    Create and configure a SparkSession.

    Returns
    -------
    pyspark.sql.SparkSession
        The configured SparkSession.
    """
    return (
        SparkSession.builder.appName("MBTA Data Streaming")
        .master("local[*]")
        .getOrCreate()
    )


def _configure_spark_logging(spark: pyspark.sql.SparkSession) -> None:
    """
    Configure Spark logging level to ERROR.

    Parameters
    ----------
    spark : pyspark.sql.SparkSession
        The SparkSession to configure.
    """
    spark.sparkContext.setLogLevel("ERROR")


def _write_to_database(batch: pyspark.sql.DataFrame, _: int) -> None:
    """
    Write batch data to a PostgreSQL database.

    Writes the given batch of data to a PostgreSQL database using JDBC.
    Spark JDBC insert does not have native support for INSERT IGNORE/REPLACE type
    operations. As a workaround, this function first inserts the batch into
    a temporary (staging) table. The staging table is then UPSERTED into
    the final production table USING A .

    We are working under budget and time constraints for this project.
    We consider this an acceptable solution given the circumstance.

    Parameters
    ----------
    batch : pyspark.sql.DataFrame
        The batch of data to be written to the database.
    _ : int
        The ID of the current batch (unused in this function).
    """
    # Database configuration
    host = configs.POSTGRES_HOST
    port = configs.POSTGRES_PORT
    database = configs.POSTGRES_DB
    url = f"jdbc:postgresql://{host}:{port}/{database}"
    user = configs.POSTGRES_USER
    password = configs.POSTGRES_PASSWORD
    driver = configs.POSTGRES_DRIVER
    table_name = configs.POSTGRES_TABLE
    temp_table_name = f"temp_{table_name}"

    # Create a JDBC connection
    connection = psycopg2.connect(
        **{"host": host, "database": database, "user": user, "password": password}
    )
    cursor = connection.cursor()

    try:
        # Create the temporary table matching the schema of the production table
        cursor.execute(
            f"""
            CREATE TEMPORARY TABLE IF NOT EXISTS {temp_table_name}
            (LIKE {table_name} INCLUDING CONSTRAINTS);
            """
        )

        # Write data from 'batch' into the temporary table
        (
            batch.write.format("jdbc")
            .option("driver", driver)
            .option("url", url)
            .option("dbtable", temp_table_name)
            .option("user", user)
            .option("password", password)
            .mode("append")
            .save()
        )

        # Perform upsert from temporary table to production
        cursor.execute(
            f"""
            INSERT INTO {table_name}
            SELECT * FROM {temp_table_name}
            ON CONFLICT (id) DO NOTHING;
            """
        )

        # Remove temporary table
        cursor.execute(f"DROP TABLE IF EXISTS {temp_table_name};")
        connection.commit()
        print("wrote to database")
    finally:
        connection.close()
        cursor.close()


def start_streaming_job() -> None:
    """
    Start the Spark streaming job.

    Sets up the Spark session, reads data from Kafka,
    processes it, and writes to a PostgreSQL database.
    """
    # Kafka configuration
    kafka_topic = configs.SCHEDULES_INPUT_TOPIC
    server_1 = f"{configs.KAFKA_HOST1}:{configs.KAFKA_PORT1}"
    server_2 = f"{configs.KAFKA_HOST2}:{configs.KAFKA_PORT2}"
    server_3 = f"{configs.KAFKA_HOST3}:{configs.KAFKA_PORT3}"

    # Create a Spark session
    spark = _create_spark_session()

    # Configure Spark logging
    _configure_spark_logging(spark)

    # Read data from Kafka
    kafka_stream = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", f"{server_1},{server_2},{server_3}")
        .option("subscribe", kafka_topic)
        .load()
    )

    print("Stream is read...")

    # Process Kafka data
    processed_df = process_schedules_stream(kafka_stream)

    # Define the Kafka query
    query_kafka: DataStreamWriter = (
        processed_df.writeStream.trigger(processingTime="10 seconds")
        .outputMode("update")
        .foreachBatch(_write_to_database)
        .start()
    )

    query_kafka.awaitTermination()

    # Stop the Spark session
    spark.stop()


if __name__ == "__main__":
    sys.exit(start_streaming_job())
