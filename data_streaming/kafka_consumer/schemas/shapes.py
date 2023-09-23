from typing import Union

import polyline
import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql.functions import udf
from shapely import LineString


@udf(returnType=T.StringType())
def _decode_polyline(encoded_polyline: str) -> Union[str, None]:
    """
    Decode polyline represenation.

    MBTA V3 API returns geometry objects in Encoded Polyline Algorithm Format.
    This UDF decodes the object and converts it to WKT (Well-Known-Text).

    Parameters
    ----------
    encoded_polyline : str
        Linestring object in encoded polyline algorithm format (e.g 'u{~vFvyys@fS]').

    Returns
    -------
    str
        WKT (well-known-text) representation of linestring object

    Notes
    -----
    Read more about Encoded Polyline Algorithm Format:
    https://developers.google.com/maps/documentation/utilities/polylinealgorithm
    """
    if encoded_polyline:
        coordinates = polyline.decode(encoded_polyline, 5, geojson=True)
        geometry = LineString(coordinates)
        return geometry.wkt

    return None


def parse_shapes_topic(
    kafka_stream: pyspark.sql.DataFrame,
) -> pyspark.sql.DataFrame:
    """
    Process Kafka stream of stops data.

    Processes the incoming Kafka stream of shape data by selecting relevant
    columns and applying schema.

    Parameters
    ----------
    kafka_stream
        The Kafka stream containing shapes data.

    Returns
    -------
    pyspark.sql.DataFrame
        The processed DataFrame containing selected and structured data.
    """
    attributes_struct = T.StructType([T.StructField("polyline", T.StringType())])

    data_schema = T.StructType(
        [
            T.StructField("type", T.StringType()),
            T.StructField("id", T.StringType()),
            T.StructField("links", T.StringType()),
            T.StructField("attributes", attributes_struct),
        ]
    )

    kafka_schema = T.StructType(
        [T.StructField("event", T.StringType()), T.StructField("data", data_schema)]
    )

    kafka_df = kafka_stream.withColumn("value", F.col("value").cast("string"))

    return kafka_df.select(
        F.from_json(F.col("value"), kafka_schema).alias("json")
    ).select(
        "json.event",
        "json.data.id",
        "json.data.type",
        _decode_polyline(F.col("json.data.attributes.polyline")).alias("geometry"),
    )
