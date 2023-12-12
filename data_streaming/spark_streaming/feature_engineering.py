import numpy as np
from haversine import Unit, haversine
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.sql.streaming import StreamingQuery


@F.udf(T.FloatType())
def _haversine_distance_udf(
    current_latitude: T.FloatType,
    current_longitude: T.FloatType,
    destination_latitude: T.FloatType,
    destination_longitude: T.FloatType,
) -> T.FloatType:
    """
    Calculate the distance between two locations using the haversine formula.

    Parameters
    ----------
    current_latitude : T.FloatType
        The latitude of the current location.
    current_longitude : T.FloatType
        The longitude of the current location.
    destination_latitude : T.FloatType
        The latitude of the destination location.
    destination_longitude : T.FloatType
        The longitude of the destination location.

    Returns
    -------
    T.FloatType
        The distance between the two locations in miles.

    Examples
    --------
    >>> _haversine_distance_udf(40.6892, -74.0445, 37.6188, -122.3750)
    2568.396
    """
    return haversine(
        (current_latitude, current_longitude),
        (destination_latitude, destination_longitude),
        unit=Unit.MILES,
    )


@F.udf(
    T.StructType(
        [
            T.StructField("sin_time", T.FloatType()),
            T.StructField("cos_time", T.FloatType()),
        ]
    )
)
def trigonometric_time(scheduled_time: T.TimestampType):
    """
    Calculate both the sin and cos of the time of day in seconds.

    Parameters
    ----------
    scheduled_time : T.TimestampType
        The time of day.

    Returns
    -------
    StructType
        A structured type containing the sin and cos of the time of day.

    Examples
    --------
    >>> trigonometric_time("2021-01-01T00:00:00Z")
    (0.0, 1.0)
    >>> trigonometric_time("2021-01-01T12:00:00Z")
    (0.0, -1.0)
    >>> trigonometric_time("2021-01-01T06:00:00Z")
    (1.0, 0.0)
    >>> trigonometric_time("2021-01-01T18:00:00Z")
    (-1.0, 0.0)
    """
    seconds_since_midnight = (
        scheduled_time.hour * 3600 + scheduled_time.minute * 60 + scheduled_time.second
    )
    seconds_in_day = 24 * 60 * 60
    angle = 2 * np.pi * seconds_since_midnight / seconds_in_day

    return (float(np.sin(angle)), float(np.cos(angle)))


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
    df = df.withColumn(
        "trigonometric_time", trigonometric_time(F.col("scheduled_time"))
    )
    df = df.withColumn("sin_time", F.col("trigonometric_time.sin_time"))
    df = df.withColumn("cos_time", F.col("trigonometric_time.cos_time"))

    # Create a vector of the features used at inference time
    assembler = VectorAssembler(
        inputCols=["distance_travel_miles", "sin_time", "cos_time"],
        outputCol="features",
    )

    df = assembler.transform(df)

    return df
