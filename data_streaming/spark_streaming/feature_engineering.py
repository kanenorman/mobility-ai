import h3
import numpy as np
from haversine import Unit, haversine
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.sql.streaming import StreamingQuery


@F.udf(T.StringType())
def _geo_to_h3_udf(latitude, longitude, resolution=9) -> str:
    return h3.geo_to_h3(latitude, longitude, resolution)


@F.udf(T.FloatType())
def _haversine_distance_udf(
    current_latitude, current_longitude, destination_latitude, destination_longitude
) -> float:
    return haversine(
        (current_latitude, current_longitude),
        (destination_latitude, destination_longitude),
        unit=Unit.MILES,
    )


@F.udf(T.FloatType())
def _sin_time(scheduled_time) -> float:
    seconds_since_midnight = (
        scheduled_time.hour() * 3600
        + scheduled_time.minute() * 60
        + scheduled_time.second()
    )
    seconds_in_day = 24 * 60 * 60
    return np.sin(2 * np.pi * seconds_since_midnight / seconds_in_day)


@F.udf(T.FloatType())
def _cos_time(scheduled_time) -> float:
    seconds_since_midnight = (
        scheduled_time.hour() * 3600
        + scheduled_time.minute() * 60
        + scheduled_time.second()
    )
    seconds_in_day = 24 * 60 * 60
    return np.cos(2 * np.pi * seconds_since_midnight / seconds_in_day)


def feature_engineering(df: DataFrame) -> StreamingQuery:
    """
    Feature engineering for the streaming data.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to perform feature engineering on.

    Returns
    -------
    StreamingQuery
    """

    df = df.withColumn(
        "current_location_hex",
        _geo_to_h3_udf(df["current_latitude"], df["current_longitude"]),
    )

    df = df.withColumn(
        "destination_location_hex",
        _geo_to_h3_udf(
            df["destination_latitude"],
            df["destination_longitude"],
        ),
    )

    # Calculate distance between current location and destination
    df = df.withColumn(
        "distance_travel_miles",
        _haversine_distance_udf(
            df["current_latitude"],
            df["current_longitude"],
            df["destination_latitude"],
            df["destination_longitude"],
        ),
    )

    # Convert the timestamp string to a timestamp type
    df = df.withColumn(
        "scheduled_time", F.to_timestamp("scheduled_time", "yyyy-MM-dd'T'HH:mm:ssXXX")
    )
    df = df.withColumn("scheduled_time", F.from_utc_timestamp("scheduled_time", "UTC"))

    df = df.withColumn("sin_time", _sin_time(df["scheduled_time"]))
    df = df.withColumn("cos_time", _cos_time(df["scheduled_time"]))

    processed_stream: StreamingQuery = (
        df.writeStream.queryName("model_features_stream")
        .outputMode("append")
        .format("console")
        .start()
    )

    return processed_stream
