import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T


def parse_routes_topic(
    kafka_stream: pyspark.sql.DataFrame,
) -> pyspark.sql.DataFrame:
    """
    Process Kafka stream of routes data.

    Processes the incoming Kafka stream of routes data by selecting relevant
    columns and applying schema.

    Parameters
    ----------
    kafka_stream
        The Kafka stream containing routes data.

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

    links_struct = T.StructType([T.StructField("self", T.StringType())])

    attributes_struct = T.StructType(
        [
            T.StructField("color", T.StringType()),
            T.StructField("description", T.StringType()),
            T.StructField("direction_destinations", T.ArrayType(T.StringType())),
            T.StructField("direction_names", T.ArrayType(T.StringType())),
            T.StructField("fare_class", T.StringType()),
            T.StructField("long_name", T.StringType()),
            T.StructField("short_name", T.StringType()),
            T.StructField("short_order", T.StringType()),
            T.StructField("text_color", T.StringType()),
            T.StructField("type", T.IntegerType()),
        ]
    )

    data_struct = T.StructType(
        [
            T.StructField("attributes", attributes_struct),
            T.StructField("id", T.StringType()),
            T.StructField("links", links_struct),
            T.StructField(
                "relationships",
                T.StructType(
                    [
                        T.StructField("line", relationships_struct),
                    ]
                ),
            ),
            T.StructField("type", T.StringType()),
        ]
    )

    kafka_schema = T.StructType(
        [T.StructField("event", T.StringType()), T.StructField("data", data_struct)]
    )

    kafka_df = kafka_stream.withColumn("value", F.col("value").cast("string"))

    return kafka_df.select(
        F.from_json(F.col("value"), kafka_schema).alias("json")
    ).select(
        "json.event",
        "json.data.id",
        "json.data.attributes.description",
        "json.data.attributes.direction_destinations",
        "json.data.attributes.fare_class",
        "json.data.attributes.long_name",
        "json.data.attributes.short_name",
        "json.data.attributes.short_order",
        "json.data.attributes.type",
        F.concat(F.lit("#"), F.col("json.data.attributes.color")).alias("color"),
        F.concat(F.lit("#"), F.col("json.data.attributes.text_color")).alias(
            "text_color"
        ),
    )
