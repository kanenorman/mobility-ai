import sys
from collections.abc import Callable

import stream_parser as stream_parser
from config import configs
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.streaming import StreamingQuery
from stream_merger import stream_merger


def _create_spark_session() -> SparkSession:
    """
    Create and configure a SparkSession.

    Returns
    -------
    SparkSession
        The configured SparkSession.
    """
    spark = (
        SparkSession.builder.appName("MBTA Data Streaming")
        .master("local[*]")
        .getOrCreate()
    )

    return spark


def _configure_spark_logging(spark: SparkSession) -> None:
    """
    Configure Spark logging level to ERROR.

    Parameters
    ----------
    spark : SparkSession
        The SparkSession to configure.
    """
    spark.sparkContext.setLogLevel("ERROR")


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
        spark.readStream.option("mode", "PERMISSIVE")
        .format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("subscribe", kafka_topic)
        .option("startingOffsets", "earliest")
        .option("maxOffsetsPerTrigger", 10_000)
        .load()
    )


def _stream(
    spark: SparkSession,
    kafka_topic: str,
    schema_parser: Callable,
) -> DataFrame:
    """
    Process data from a Kafka stream and write it to a table.

    Parameters
    ----------
    spark : SparkSession
        The Spark session for data processing.
    kafka_topic : str
        The name of the Kafka topic to read data from.
    schema_parser : Callable
        A callable function that parses and transforms the Kafka data stream
        into a DataFrame.
    Returns
    -------
    StreamingQuery
    """
    kafka_stream: DataFrame = _read_stream_from_kafka(spark, kafka_topic)
    df: DataFrame = schema_parser(kafka_stream)

    return df


def main() -> int:
    """
    Start the Spark streaming job.
    """
    spark = _create_spark_session()
    _configure_spark_logging(spark)

    vehicle: DataFrame = _stream(
        spark=spark,
        kafka_topic="VEHICLE_JSON",
        schema_parser=stream_parser.parse_vehicle_json,
    )

    stop: DataFrame = _stream(
        spark=spark,
        kafka_topic="STOP_JSON",
        schema_parser=stream_parser.parse_stop_json,
    )

    schedule: DataFrame = _stream(
        spark=spark,
        kafka_topic="SCHEDULE_JSON",
        schema_parser=stream_parser.parse_schedule_json,
    )

    trip: DataFrame = _stream(
        spark=spark,
        kafka_topic="TRIP_JSON",
        schema_parser=stream_parser.parse_trip_json,
    )

    merged_stream: StreamingQuery = stream_merger(vehicle, stop, schedule, trip)
    merged_stream.awaitTermination()

    spark.stop()

    return 0


if __name__ == "__main__":
    sys.exit(main())
