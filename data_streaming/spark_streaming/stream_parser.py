import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T


def parse_vehicle_json(
    kafka_stream: pyspark.sql.DataFrame,
) -> pyspark.sql.DataFrame:
    """
    Parse the vehicle JSON data stream.

    Parameters
    ----------
    kafka_stream : pyspark.sql.DataFrame
        The Kafka data stream.

    Returns
    -------
    pyspark.sql.DataFrame
    """

    JSON_SCHEMA = T.StructType(
        [
            T.StructField("EVENT", T.StringType()),
            T.StructField("BEARING", T.IntegerType()),
            T.StructField("CURRENT_STATUS", T.StringType()),
            T.StructField("CURRENT_STOP_SEQUENCE", T.IntegerType()),
            T.StructField("DIRECTION_ID", T.IntegerType()),
            T.StructField("LABEL", T.StringType()),
            T.StructField("LATITUDE", T.DoubleType()),
            T.StructField("LONGITUDE", T.DoubleType()),
            T.StructField("SPEED", T.IntegerType()),
            T.StructField("UPDATED_AT", T.LongType()),
            T.StructField("SELF", T.StringType()),
            T.StructField("STOP_ID", T.StringType()),
            T.StructField("STOP_TYPE", T.StringType()),
            T.StructField("TRIP_ID", T.StringType()),
            T.StructField("TRIP_TYPE", T.StringType()),
            T.StructField("TYPE", T.StringType()),
        ]
    )

    return kafka_stream.select(
        F.col("key").cast(T.StringType()).alias("id"),
        F.from_json(kafka_stream.value.cast(T.StringType()), JSON_SCHEMA).alias("json"),
    ).select(
        "id",
        "json.event",
        "json.bearing",
        "json.current_status",
        "json.current_stop_sequence",
        "json.direction_id",
        "json.label",
        "json.latitude",
        "json.longitude",
        "json.speed",
        "json.updated_at",
        "json.self",
        "json.stop_id",
        "json.stop_type",
        "json.trip_id",
        "json.trip_type",
        "json.type",
    )


def parse_stop_json(kafka_stream: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    """
    Parse the stop JSON data stream.

    Parameters
    ----------
    kafka_stream : pyspark.sql.DataFrame
        The Kafka data stream.

    Returns
    -------
    pyspark.sql.DataFrame
    """

    JSON_SCHEMA = T.StructType(
        [
            T.StructField("EVENT", T.StringType()),
            T.StructField("ADDRESS", T.StringType()),
            T.StructField("AT_STREET", T.StringType()),
            T.StructField("DESCRIPTION", T.StringType()),
            T.StructField("LATITUDE", T.DoubleType()),
            T.StructField("LOCATION_TYPE", T.IntegerType()),
            T.StructField("LONGITUDE", T.DoubleType()),
            T.StructField("MUNICIPALITY", T.StringType()),
            T.StructField("NAME", T.StringType()),
            T.StructField("ON_STREET", T.StringType()),
            T.StructField("PLATFORM_CODE", T.StringType()),
            T.StructField("PLATFORM_NAME", T.StringType()),
            T.StructField("VEHICLE_TYPE", T.StringType()),
            T.StructField("WHEELCHAIR_BOARDING", T.IntegerType()),
            T.StructField("SELF", T.StringType()),
            T.StructField("FACILITIES_SELF", T.StringType()),
            T.StructField("PARENT_STATION_ID", T.StringType()),
            T.StructField("PARENT_STATION_TYPE", T.StringType()),
            T.StructField("ZONE_ID", T.StringType()),
            T.StructField("TYPE", T.StringType()),
        ]
    )

    return kafka_stream.select(
        F.col("key").cast(T.StringType()).alias("id"),
        F.from_json(kafka_stream.value.cast(T.StringType()), JSON_SCHEMA).alias("json"),
    ).select(
        "id",
        "json.event",
        "json.address",
        "json.at_street",
        "json.description",
        "json.latitude",
        "json.location_type",
        "json.longitude",
        "json.municipality",
        "json.name",
        "json.on_street",
        "json.platform_code",
        "json.platform_name",
        "json.vehicle_type",
        "json.wheelchair_boarding",
        "json.self",
        "json.facilities_self",
        "json.parent_station_id",
        "json.parent_station_type",
        "json.zone_id",
        "json.type",
    )


def parse_trip_json(kafka_stream: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    """
    Parse the trip JSON data stream.

    Parameters
    ----------
    kafka_stream : pyspark.sql.DataFrame
        The Kafka data stream.

    Returns
    -------
    pyspark.sql.DataFrame
    """

    JSON_SCHEMA = T.StructType(
        [
            T.StructField("EVENT", T.StringType()),
            T.StructField("BIKES_ALLOWED", T.IntegerType()),
            T.StructField("BLOCK_ID", T.StringType()),
            T.StructField("DIRECTION_ID", T.IntegerType()),
            T.StructField("HEADSIGN", T.StringType()),
            T.StructField("NAME", T.StringType()),
            T.StructField("WHEELCHAIR_ACCESSIBLE", T.IntegerType()),
            T.StructField("SELF", T.StringType()),
            T.StructField("SHAPE_ID", T.StringType()),
            T.StructField("SHAPE_TYPE", T.StringType()),
            T.StructField("SERVICE_ID", T.StringType()),
            T.StructField("SERVICE_TYPE", T.StringType()),
            T.StructField("ROUTE_ID", T.StringType()),
            T.StructField("ROUTE_TYPE", T.StringType()),
            T.StructField("ROUTE_PATTERN_ID", T.StringType()),
            T.StructField("ROUTE_PATTERN_TYPE", T.StringType()),
            T.StructField("TYPE", T.StringType()),
        ]
    )

    return kafka_stream.select(
        F.col("key").cast(T.StringType()).alias("id"),
        F.from_json(kafka_stream.value.cast(T.StringType()), JSON_SCHEMA).alias("json"),
    ).select(
        "id",
        "json.event",
        "json.bikes_allowed",
        "json.block_id",
        "json.direction_id",
        "json.headsign",
        "json.name",
        "json.wheelchair_accessible",
        "json.self",
        "json.shape_id",
        "json.shape_type",
        "json.service_id",
        "json.service_type",
        "json.route_id",
        "json.route_type",
        "json.route_pattern_id",
        "json.route_pattern_type",
        "json.type",
    )


def parse_schedule_json(kafka_stream: pyspark.sql.DataFrame):
    """
    Parse the schedule JSON data stream.

    Parameters
    ----------
    kafka_stream : pyspark.sql.DataFrame
        The Kafka data stream.

    Returns
    -------
    pyspark.sql.DataFrame
    """

    JSON_SCHEMA = T.StructType(
        [
            T.StructField("EVENT", T.StringType()),
            T.StructField("ARRIVAL_TIME", T.TimestampType()),
            T.StructField("DEPARTURE_TIME", T.TimestampType()),
            T.StructField("DIRECTION_ID", T.IntegerType()),
            T.StructField("DROP_OFF_TYPE", T.IntegerType()),
            T.StructField("PICKUP_TYPE", T.IntegerType()),
            T.StructField("STOP_HEADSIGN", T.StringType()),
            T.StructField("STOP_SEQUENCE", T.IntegerType()),
            T.StructField("TIMEPOINT", T.BooleanType()),
            T.StructField("ROUTE_ID", T.StringType()),
            T.StructField("ROUTE_TYPE", T.StringType()),
            T.StructField("STOP_ID", T.StringType()),
            T.StructField("STOP_TYPE", T.StringType()),
            T.StructField("TRIP_ID", T.StringType()),
            T.StructField("TRIP_TYPE", T.StringType()),
            T.StructField("TYPE", T.StringType()),
        ]
    )

    return kafka_stream.select(
        F.col("key").cast(T.StringType()).alias("id"),
        F.from_json(kafka_stream.value.cast(T.StringType()), JSON_SCHEMA).alias("json"),
    ).select(
        "id",
        "json.event",
        "json.arrival_time",
        "json.departure_time",
        "json.direction_id",
        "json.drop_off_type",
        "json.pickup_type",
        "json.stop_headsign",
        "json.stop_sequence",
        "json.timepoint",
        "json.route_id",
        "json.route_type",
        "json.stop_id",
        "json.stop_type",
        "json.trip_id",
        "json.trip_type",
        "json.type",
    )
