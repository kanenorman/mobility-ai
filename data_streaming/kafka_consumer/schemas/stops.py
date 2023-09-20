import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T


def parse_stops_topic(
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
    data_struct = T.StructType(
        [
            T.StructField("id", T.StringType()),
            T.StructField("type", T.StringType()),
        ]
    )

    links_struct = T.StructType([T.StructField("self", T.StringType())])

    attributes_struct = T.StructType(
        [
            T.StructField("address", T.StringType()),
            T.StructField("at_street", T.StringType()),
            T.StructField("description", T.StringType()),
            T.StructField("latitude", T.FloatType()),
            T.StructField("location_type", T.IntegerType()),
            T.StructField("longitude", T.FloatType()),
            T.StructField("municipality", T.StringType()),
            T.StructField("name", T.StringType()),
            T.StructField("on_street", T.StringType()),
            T.StructField("platform_code", T.StringType()),
            T.StructField("platform_name", T.StringType()),
            T.StructField("vehicle_type", T.StringType()),
            T.StructField("wheelchair_boarding", T.IntegerType()),
        ]
    )

    relationships_struct = T.StructType(
        [
            T.StructField("facilities", links_struct),
            T.StructField(
                "parent_station",
                T.StructType(
                    [
                        T.StructField("data", data_struct),
                    ]
                ),
            ),
            T.StructField(
                "zone",
                T.StructType(
                    [
                        T.StructField("data", data_struct),
                    ]
                ),
            ),
        ]
    )

    data_schema = T.StructType(
        [
            T.StructField("type", T.StringType()),
            T.StructField("id", T.StringType()),
            T.StructField("links", T.StringType()),
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
        "json.data.attributes.address",
        "json.data.attributes.at_street",
        "json.data.attributes.description",
        "json.data.attributes.latitude",
        "json.data.attributes.location_type",
        "json.data.attributes.longitude",
        "json.data.attributes.municipality",
        "json.data.attributes.name",
        "json.data.attributes.on_street",
        "json.data.attributes.platform_code",
        "json.data.attributes.platform_name",
        "json.data.attributes.vehicle_type",
        "json.data.attributes.wheelchair_boarding",
        F.col("json.data.relationships.zone.data.id").alias("zone"),
        F.col("json.data.relationships.parent_station.data.id").alias("parent_station"),
    )
