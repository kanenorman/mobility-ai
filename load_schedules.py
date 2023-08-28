import pyspark.sql.functions as F
import pyspark.sql.types as T


def process_schedules_stream(kafka_stream):
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
            T.StructField("id", T.IntegerType()),
            T.StructField("type", T.StringType()),
        ]
    )

    relationships_struct = T.StructType(
        [
            T.StructField("data", data_struct),
        ]
    )

    # Define the main schema
    schedule_schema = T.StructType(
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

    kafka_df = kafka_stream.withColumn("value", F.col("value").cast("string"))

    processed_df = kafka_df.select(
        F.from_json(F.col("value"), schedule_schema).alias("json")
    ).select(
        "json.id",
        "json.attributes.arrival_time",
        "json.attributes.departure_time",
        "json.attributes.direction_id",
        "json.attributes.drop_off_type",
        "json.attributes.pickup_type",
        "json.attributes.stop_headsign",
        "json.attributes.stop_sequence",
        "json.attributes.timepoint",
        F.col("json.relationships.route.data.id").alias("route_id"),
        F.col("json.relationships.stop.data.id").alias("stop_id"),
        F.col("json.relationships.trip.data.id").alias("trip_id"),
    )
    return processed_df
