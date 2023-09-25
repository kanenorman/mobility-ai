import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T


def parse_vehicles_topic(
    kafka_stream: pyspark.sql.DataFrame,
) -> pyspark.sql.DataFrame:
    """
    Process Kafka stream of vehicles data.

    Parameters
    ----------
    kafka_stream
        The Kafka stream containing vehicles data.

    Returns
    -------
    pyspark.sql.DataFrame
        The processed DataFrame containing selected and structured data.
    """
    data_struct = T.StructType(
        [
            T.StructField("id", T.StringType()),
            T.StructField("type", T.StringType()),
        ]
    )

    relationships_struct = T.StructType(
        [
            T.StructField("data", data_struct),
        ]
    )

    carriages_struct = T.ArrayType(
        T.StructType(
            [
                T.StructField("occupancy_status", T.StringType()),
                T.StructField("occupancy_percentage", T.IntegerType()),
                T.StructField("label", T.StringType()),
            ]
        )
    )
    attributes_struct = T.StructType(
        [
            T.StructField("bearing", T.IntegerType()),
            T.StructField("current_status", T.StringType()),
            T.StructField("current_stop_sequence", T.IntegerType()),
            T.StructField("direction_id", T.IntegerType()),
            T.StructField("label", T.StringType()),
            T.StructField("latitude", T.DoubleType()),
            T.StructField("longitude", T.DoubleType()),
            T.StructField("occupancy_status", carriages_struct),
            T.StructField("speed", T.IntegerType()),
            T.StructField("updated_at", T.TimestampType()),
        ]
    )

    data_schema = T.StructType(
        [
            T.StructField("type", T.StringType()),
            T.StructField("id", T.StringType()),
            T.StructField("links", T.StringType()),
            T.StructField("attributes", attributes_struct),
            T.StructField(
                "relationships",
                T.StructType(
                    [
                        T.StructField("route", relationships_struct),
                        T.StructField("stop", relationships_struct),
                        T.StructField("trip", relationships_struct),
                    ]
                ),
            ),
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
        "json.data.attributes.bearing",
        "json.data.attributes.current_status",
        "json.data.attributes.current_stop_sequence",
        "json.data.attributes.direction_id",
        "json.data.attributes.label",
        "json.data.attributes.latitude",
        "json.data.attributes.longitude",
        "json.data.attributes.occupancy_status",
        "json.data.attributes.speed",
        "json.data.attributes.updated_at",
        F.col("json.data.relationships.route.data.id").alias("route_id"),
        F.col("json.data.relationships.stop.data.id").alias("stop_id"),
        F.col("json.data.relationships.trip.data.id").alias("trip_id"),
    )
