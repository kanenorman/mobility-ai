import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T


def parse_schedules_topic(
    kafka_stream: pyspark.sql.DataFrame,
) -> pyspark.sql.DataFrame:
    """
    Process Kafka stream of schedules data.

    Processes the incoming Kafka stream of schedules data by selecting relevant
    columns and applying schema.

    Parameters
    ----------
    kafka_stream
        The Kafka stream containing schedules data.

    Returns
    -------
    pyspark.sql.DataFrame
        The processed DataFrame containing selected and structured data.
    """
    attributes_struct = T.StructType(
        [
            T.StructField("arrival_time", T.TimestampType()),
            T.StructField("departure_time", T.TimestampType()),
            T.StructField("direction_id", T.IntegerType()),
            T.StructField("drop_off_type", T.IntegerType()),
            T.StructField("pickup_type", T.IntegerType()),
            T.StructField("stop_headsign", T.StringType()),
            T.StructField("stop_sequence", T.IntegerType()),
            T.StructField("timepoint", T.BooleanType()),
        ]
    )

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

    data_schema = T.StructType(
        [
            T.StructField("attributes", attributes_struct),
            T.StructField("id", T.StringType()),
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
            T.StructField("type", T.StringType()),
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
        "json.data.attributes.arrival_time",
        "json.data.attributes.departure_time",
        "json.data.attributes.direction_id",
        "json.data.attributes.drop_off_type",
        "json.data.attributes.pickup_type",
        "json.data.attributes.stop_headsign",
        "json.data.attributes.stop_sequence",
        "json.data.attributes.timepoint",
        F.col("json.data.relationships.route.data.id").alias("route_id"),
        F.col("json.data.relationships.stop.data.id").alias("stop_id"),
        F.col("json.data.relationships.trip.data.id").alias("trip_id"),
    )
