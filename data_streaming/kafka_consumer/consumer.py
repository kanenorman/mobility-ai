import sys
from collections.abc import Callable

import schemas
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.streaming import DataStreamWriter, StreamingQuery
from utils import (configs, configure_spark_logging, create_spark_session,
                   write_to_database)


def _read_stream_from_kafka(spark: SparkSession, kafka_topic: str) -> DataFrame:
    """
    Read data from Kafka into a Spark DataFrame.

    Parameters
    ----------
    spark : SparkSession
        The Spark session.
    kafka_topic : str
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
        .option("subscribe", kafka_topic)
        .option("startingOffsets", "earliest")
        .option("maxOffsetsPerTrigger", 1000)
        .load()
    )


def _write_data_stream(
    df: DataFrame, destination_table: str, primary_key: str
) -> DataStreamWriter:
    """
    Write a Spark DataFrame to a database.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to write.
    destination_table : str
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
                batch, epoch_id, destination_table, primary_key
            )
        )
        .start()
    )


def _stream(
    spark: SparkSession,
    kafka_topic: str,
    data_schema: Callable,
    destination_table: str,
    primary_key_column: str,
) -> StreamingQuery:
    """
    Process data from a Kafka stream and write it to a table.

    Parameters
    ----------
    spark : SparkSession
        The Spark session for data processing.
    kafka_topic : str
        The name of the Kafka topic to read data from.
    data_schema : Callable
        A callable function that parses and transforms the Kafka data stream
        into a DataFrame.
    destination_table : str
        The name of the table to write the processed data to.
    primary_key_column : str
        The primary key column for the target table.

    Returns
    -------
    StreamingQuery
    """
    kafka_stream = _read_stream_from_kafka(spark, kafka_topic)
    data_df = data_schema(kafka_stream)
    stream_writer = _write_data_stream(data_df, destination_table, primary_key_column)
    return stream_writer


def start_streaming_job() -> None:
    """
    Start the Spark streaming job.

    Sets up the Spark session, reads data from Kafka,
    processes it, and writes to a PostgreSQL database.
    """
    spark = create_spark_session()
    configure_spark_logging(spark)

    schedule_stream = _stream(
        spark=spark,
        kafka_topic="schedules",
        data_schema=schemas.parse_schedules_topic,
        destination_table="schedule",
        primary_key_column="id",
    )
    trips_stream = _stream(
        spark=spark,
        kafka_topic="trips",
        data_schema=schemas.parse_trips_topic,
        destination_table="trip",
        primary_key_column="id",
    )
    stops_stream = _stream(
        spark=spark,
        kafka_topic="stops",
        data_schema=schemas.parse_stops_topic,
        destination_table="stop",
        primary_key_column="id",
    )
    shapes_stream = _stream(
        spark=spark,
        kafka_topic="shapes",
        data_schema=schemas.parse_shapes_topic,
        destination_table="shape",
        primary_key_column="id",
    )

    schedule_stream.awaitTermination()
    trips_stream.awaitTermination()
    stops_stream.awaitTermination()
    shapes_stream.awaitTermination()

    spark.stop()


if __name__ == "__main__":
    sys.exit(start_streaming_job())
