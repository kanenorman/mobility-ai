import sys

from load_schedules import process_schedules_stream
from pyspark.sql.streaming import DataStreamWriter
from utils import (configs, configure_spark_logging, create_spark_session,
                   write_to_database)


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
    spark = create_spark_session()

    # Configure Spark logging
    configure_spark_logging(spark)

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

    table_name = configs.POSTGRES_TABLE
    unique_id = "id"

    # Define the Kafka query
    query_kafka: DataStreamWriter = (
        processed_df.writeStream.trigger(processingTime="10 seconds")
        .outputMode("update")
        .foreachBatch(
            lambda df, epoch_id: write_to_database(df, epoch_id, table_name, unique_id)
        )
        .start()
    )

    query_kafka.awaitTermination()

    # Stop the Spark session
    spark.stop()


if __name__ == "__main__":
    sys.exit(start_streaming_job())
