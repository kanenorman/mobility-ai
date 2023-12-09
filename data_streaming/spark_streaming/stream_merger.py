import pyspark
from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery


def stream_merger(
    vehicle: DataFrame,
    stop: DataFrame,
    schedule: DataFrame,
    trip: DataFrame,
) -> StreamingQuery:
    """
    Merge the streams into a single DataFrame.

    Parameters
    ----------
    vehicle : DataFrame
        The vehicle stream.
    stop : DataFrame
        The stop stream.
    schedule : DataFrame
        The schedule stream.
    trip : DataFrame
        The trip stream.

    Returns
    -------
    DataFrame
        A DataFrame containing merged data from the input streams.
    """

    features: pyspark.sql.DataFrame = (
        vehicle.join(stop, vehicle.stop_id == stop.id)
        .join(trip, vehicle.trip_id == trip.id)
        .join(
            schedule,
            (schedule.trip_id == vehicle.trip_id)
            & (schedule.stop_id == vehicle.stop_id),
        )
    ).select(
        vehicle.updated_at.alias("time_stamp"),
        vehicle.id.alias("vehicle_id"),
        vehicle.current_status,
        vehicle.latitude.alias("current_latitude"),
        vehicle.longitude.alias("current_longitude"),
        stop.name.alias("destination"),
        stop.platform_name,
        stop.latitude.alias("destination_latitude"),
        stop.longitude.alias("destination_longitude"),
        trip.name.alias("trip_name"),
        schedule.departure_time.alias("scheduled_departure"),
        schedule.arrival_time.alias("scheduled_arrival"),
        stop.id.alias("stop_id"),
        trip.id.alias("trip_id"),
        schedule.stop_id.alias("sch_stop_id"),
        schedule.trip_id.alias("sch_trip_id"),
    )

    stream: StreamingQuery = (
        features.writeStream.queryName("model_features_stream")
        .format("console")
        .outputMode("append")
        .start()
    )

    return stream
