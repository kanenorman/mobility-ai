import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T


def parse_alerts_topic(
    kafka_stream: pyspark.sql.DataFrame,
) -> pyspark.sql.DataFrame:
    """
    Process Kafka stream of schedules data.

    Processes the incoming Kafka stream of alerts data by selecting relevant
    columns and applying schema.

    Parameters
    ----------
    kafka_stream
        The Kafka stream containing alerts data.

    Returns
    -------
    pyspark.sql.DataFrame
        The processed DataFrame containing selected and structured data.
    """
    active_struct = T.ArrayType(
        T.StructType(
            [
                T.StructField("end", T.TimestampType()),
                T.StructField("start", T.TimestampType()),
            ]
        )
    )

    informed_entity_struct = T.ArrayType(
        T.StructType(
            [
                T.StructField("activities", T.ArrayType(T.StringType())),
                T.StructField("route", T.StringType()),
                T.StructField("route_type", T.IntegerType()),
                T.StructField("stop", T.StringType()),
            ]
        )
    )

    links_struct = T.StructType([T.StructField("self", T.StringType())])

    # Define the schema for the "attributes" field
    attributes_struct = T.StructType(
        [
            T.StructField("active_period", active_struct),
            T.StructField("banner", T.StringType()),
            T.StructField("cause", T.StringType()),
            T.StructField("created_at", T.TimestampType()),
            T.StructField("description", T.StringType()),
            T.StructField("effect", T.StringType()),
            T.StructField("header", T.StringType()),
            T.StructField("image", T.StringType()),
            T.StructField("image_alternative_text", T.StringType()),
            T.StructField("informed_entity", informed_entity_struct),
            T.StructField("lifecycle", T.StringType()),
            T.StructField("service_effect", T.StringType()),
            T.StructField("severity", T.IntegerType()),
            T.StructField("short_header", T.StringType()),
            T.StructField("timeframe", T.StringType()),
            T.StructField("updated_at", T.TimestampType()),
            T.StructField("url", T.StringType()),
        ]
    )

    # Define the schema for the "data" field
    data_struct = T.StructType(
        [
            T.StructField("attributes", attributes_struct),
            T.StructField("id", T.StringType()),
            T.StructField("links", links_struct),
            T.StructField("type", T.StringType()),
        ]
    )

    # Define the top-level schema for the JSON
    kafka_schema = T.StructType(
        [T.StructField("event", T.StringType()), T.StructField("data", data_struct)]
    )

    kafka_df = kafka_stream.withColumn("value", F.col("value").cast("string"))

    return kafka_df.select(
        F.from_json(F.col("value"), kafka_schema).alias("json")
    ).select(
        "json.event",
        "json.data.id",
        "json.data.attributes.active_period",
        "json.data.attributes.banner",
        "json.data.attributes.cause",
        "json.data.attributes.created_at",
        "json.data.attributes.description",
        "json.data.attributes.effect",
        "json.data.attributes.header",
        "json.data.attributes.image",
        "json.data.attributes.image_alternative_text",
        "json.data.attributes.informed_entity",
        "json.data.attributes.lifecycle",
        "json.data.attributes.service_effect",
        "json.data.attributes.severity",
        "json.data.attributes.short_header",
        "json.data.attributes.timeframe",
        "json.data.attributes.updated_at",
        "json.data.type",
    )
