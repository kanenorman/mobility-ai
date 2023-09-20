import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T


def parse_trips_topic(
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
            T.StructField("bikes_allowed", T.IntegerType()),
            T.StructField("block_id", T.StringType()),
            T.StructField("direction_id", T.IntegerType()),
            T.StructField("headsign", T.StringType()),
            T.StructField("name", T.StringType()),
            T.StructField("wheelchair_accessible", T.IntegerType()),
        ]
    )

    data_struct = T.StructType(
        [
            T.StructField(
                "data",
                T.StructType(
                    [
                        T.StructField("id", T.StringType()),
                        T.StructField("type", T.StringType()),
                    ]
                ),
            )
        ]
    )

    links_struct = T.StructType(
        [
            T.StructField("self", T.StringType()),
        ]
    )

    relationships_struct = T.StructType(
        [
            T.StructField("shape", data_struct),
            T.StructField("service", data_struct),
            T.StructField("route", data_struct),
            T.StructField("route_pattern", data_struct),
        ]
    )

    data_schema = T.StructType(
        [
            T.StructField("type", T.StringType()),
            T.StructField("id", T.StringType()),
            T.StructField("links", links_struct),
            T.StructField("attributes", attributes_struct),
            T.StructField("relationships", relationships_struct),
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
        "json.data.attributes.bikes_allowed",
        "json.data.attributes.block_id",
        "json.data.attributes.direction_id",
        "json.data.attributes.headsign",
        "json.data.attributes.name",
        "json.data.attributes.wheelchair_accessible",
        F.col("json.data.relationships.shape.data.id").alias("shape_id"),
        F.col("json.data.relationships.service.data.id").alias("service_id"),
        F.col("json.data.relationships.route.data.id").alias("route_id"),
        F.col("json.data.relationships.route_pattern.data.id").alias(
            "route_pattern_id"
        ),
    )
