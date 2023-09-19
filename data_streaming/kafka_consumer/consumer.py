import sys

import schemas
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.streaming import DataStreamWriter
from utils import (configs, configure_spark_logging, create_spark_session,
                   write_to_database)


def _read_stream_from_kafka(spark: SparkSession, topic: str) -> DataFrame:
    """
    Read data from Kafka into a Spark DataFrame.

    Parameters
    ----------
    spark : SparkSession
        The Spark session.
    topic : str
        The Kafka topic to subscribe to.

    Returns
    -------
    DataFrame
        A Spark DataFrame containing the Kafka data.
    """
    server_1 = f"{configs.KAFKA_HOST1}:{configs.KAFKA_PORT1}"
    server_2 = f"{configs.KAFKA_HOST2}:{configs.KAFKA_PORT2}"
    server_3 = f"{configs.KAFKA_HOST3}:{configs.KAFKA_PORT3}"
    bootstrap_servers = f"{server_1},{server_2},{server_3}"

    return (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("subscribe", topic)
        .option("startingOffsets", "earliest")
        .option("maxOffsetsPerTrigger", 1000)
        .load()
    )


def _write_data_stream(
    df: DataFrame, table_name: str, primary_key: str
) -> DataStreamWriter:
    """
    Write a Spark DataFrame to a database.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to write.
    table_name : str
        The name of the database table.
    primary_key : str
        The primary key of the table.

    Returns
    -------
    DataStreamWriter
        The DataStreamWriter for the write operation.
    """
    return (
        df.writeStream.trigger(processingTime="10 seconds")
        .outputMode("update")
        .foreachBatch(
            lambda batch, epoch_id: write_to_database(
                batch, epoch_id, table_name, primary_key
            )
        )
        .start()
    )


def start_streaming_job() -> None:
    """
    Start the Spark streaming job.

    Sets up the Spark session, reads data from Kafka,
    processes it, and writes to a PostgreSQL database.
    """
    spark = create_spark_session()
    configure_spark_logging(spark)

    schedules_stream = _read_stream_from_kafka(spark, "schedules")
    schedule_df = schemas.parse_schedules_topic(schedules_stream)
    schedule_stream_writer = _write_data_stream(
        schedule_df, table_name="schedule", primary_key="id"
    )

    alerts_stream = _read_stream_from_kafka(spark, "alerts")
    alerts_df = schemas.parse_alerts_topic(alerts_stream)
    alert_stream_writer = _write_data_stream(
        alerts_df, table_name="alert", primary_key="id"
    )

    schedule_stream_writer.awaitTermination()
    alert_stream_writer.awaitTermination()

    spark.stop()


if __name__ == "__main__":
    sys.exit(start_streaming_job())
