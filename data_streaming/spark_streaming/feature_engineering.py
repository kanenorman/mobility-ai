import h3
from haversine import Unit, haversine
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.sql.streaming import StreamingQuery


@F.udf(T.StringType())
def _geo_to_h3_udf(latitude, longitude, resolution=9):
    return h3.geo_to_h3(latitude, longitude, resolution)


@F.udf(T.FloatType())
def _haversine_distance_udf(
    current_latitude, current_longitude, destination_latitude, destination_longitude
):
    return haversine(
        (current_latitude, current_longitude),
        (destination_latitude, destination_longitude),
        unit=Unit.MILES,
    )


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

    df = df.withColumn(
        "distance_travel_miles",
        _haversine_distance_udf(
            df["current_latitude"],
            df["current_longitude"],
            df["destination_latitude"],
            df["destination_longitude"],
        ),
    )

    processed_stream: StreamingQuery = (
        df.writeStream.queryName("model_features_stream")
        .outputMode("append")
        .format("console")
        .start()
    )

    return processed_stream
