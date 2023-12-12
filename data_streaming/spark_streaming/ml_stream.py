import sys
from collections.abc import Callable

import stream_parser as stream_parser
from config import configs
from feature_engineering import feature_engineering
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.streaming import StreamingQuery
from stream_merger import stream_merger
from stream_predictor import stream_predictor


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


def _read_stream_from_kafka(
    spark: SparkSession, kafka_topic: str, group_id: str, bootstrap_servers: str
) -> DataFrame:
    """
    Read data from Kafka into a Spark DataFrame.

    Parameters
    ----------
    spark : SparkSession
        The Spark session.
    kafka_topic : str
        The Kafka topic to subscribe to.
    group_id : str
        The unique consumer group ID for this stream.
    bootstrap_servers: str
        Kafka bootstrap servers

    Returns
    -------
    DataFrame
        A Spark DataFrame containing the Kafka data.
    """

    return (
        spark.readStream.option("mode", "PERMISSIVE")
        .format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("subscribe", kafka_topic)
        .option("startingOffsets", "earliest")
        .option("maxOffsetsPerTrigger", 500)
        .option("kafka.group.id", group_id)
        .load()
    )


def _stream(
    spark: SparkSession,
    kafka_topic: str,
    schema_parser: Callable,
    group_id: str,
    bootstrap_servers: str,
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
    group_id : str
        The unique consumer group ID for this stream.
    bootstrap_servers :str
        Kafka bootstrap servers

    Returns
    -------
    StreamingQuery
    """
    kafka_stream: DataFrame = _read_stream_from_kafka(
        spark, kafka_topic, group_id, bootstrap_servers
    )
    df: DataFrame = schema_parser(kafka_stream)

    return df


def main() -> int:
    """
    Start the Spark streaming job.
    """
    spark = _create_spark_session()
    _configure_spark_logging(spark)

    server_1 = f"{configs.KAFKA_HOST1}:{configs.KAFKA_PORT1}"
    server_2 = f"{configs.KAFKA_HOST2}:{configs.KAFKA_PORT2}"
    server_3 = f"{configs.KAFKA_HOST3}:{configs.KAFKA_PORT3}"
    bootstrap_servers = f"{server_1},{server_2},{server_3}"

    vehicle: DataFrame = _stream(
        spark=spark,
        kafka_topic="VEHICLE_JSON",
        schema_parser=stream_parser.parse_vehicle_json,
        group_id="vehicle-consumer-group",
        bootstrap_servers=bootstrap_servers,
    )

    stop: DataFrame = _stream(
        spark=spark,
        kafka_topic="STOP_JSON",
        schema_parser=stream_parser.parse_stop_json,
        group_id="stop-consumer-group",
        bootstrap_servers=bootstrap_servers,
    )

    schedule: DataFrame = _stream(
        spark=spark,
        kafka_topic="SCHEDULE_JSON",
        schema_parser=stream_parser.parse_schedule_json,
        group_id="schedule-consumer-group",
        bootstrap_servers=bootstrap_servers,
    )

    trip: DataFrame = _stream(
        spark=spark,
        kafka_topic="TRIP_JSON",
        schema_parser=stream_parser.parse_trip_json,
        group_id="trip-consumer-group",
        bootstrap_servers=bootstrap_servers,
    )

    unprocessed_data: DataFrame = stream_merger(vehicle, stop, schedule, trip)
    processed_stream: DataFrame = feature_engineering(unprocessed_data)
    prediction_stream: StreamingQuery = stream_predictor(
        processed_stream, bootstrap_servers
    )

    prediction_stream.awaitTermination()

    spark.stop()

    return 0


if __name__ == "__main__":
    sys.exit(main())
