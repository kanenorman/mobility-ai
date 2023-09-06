import sys

import pyspark
from config import configs
from load_schedules import process_schedules_stream
from pyspark.sql import SparkSession
from pyspark.sql.streaming import DataStreamWriter


def _write_to_database(batch: pyspark.sql.DataFrame, _: int) -> None:
    """
    Write batch data to a PostgreSQL database.

    Writes the given batch of data to a PostgreSQL database using JDBC.

    Parameters
    ----------
    batch
        The batch of data to be written to the database.
    _
        The ID of the current batch (unused in this function).
    """
    host = configs.POSTGRES_HOST
    port = configs.POSTGRES_PORT
    database = configs.POSTGRES_DB
    url = f"jdbc:postgresql://{host}:{port}/{database}"

    print("writing to databse...")
    (
        batch.write.format("jdbc")
        .option("driver", configs.POSTGRES_DRIVER)
        .option("url", url)
        .option("dbtable", configs.POSTGRES_TABLE)
        .option("user", configs.POSTGRES_USER)
        .option("password", configs.POSTGRES_PASSWORD)
        .mode("append")
        .option("saveMode", "ignore")
        .save()
    )


def main() -> None:
    """
    Start the Spark streaming job.

    Sets up the Spark session, reads data from Kafka,
    processes it, and writes to a PostgreSQL database.
    """
    spark = (
        SparkSession.builder.appName("MBTA Data Streaming")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    kafka_topic = configs.SCHEDULES_INPUT_TOPIC
    server_1 = f"{configs.KAFKA_HOST1}:{configs.KAFKA_PORT1}"
    server_2 = f"{configs.KAFKA_HOST2}:{configs.KAFKA_PORT2}"
    server_3 = f"{configs.KAFKA_HOST3}:{configs.KAFKA_PORT3}"

    kafka_stream = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", f"{server_1},{server_2},{server_3}")
        .option("subscribe", kafka_topic)
        .load()
    )

    print("stream is read...")
    processed_df = process_schedules_stream(kafka_stream)

    query_kafka: DataStreamWriter = (
        processed_df.writeStream.trigger(processingTime="10 seconds")
        .outputMode("update")
        .foreachBatch(_write_to_database)
        .start()
    )

    query_kafka.awaitTermination()

    spark.stop()


if __name__ == "__main__":
    sys.exit(main())
