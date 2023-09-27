from dataclasses import dataclass

from ..extensions import database as db


@dataclass()
class Schedule(db.Model):
    """
    Schedule entry for public transportation.

    Parameters
    ----------
    event : str
        MBTA V3 API Streaming Event
    id : str
        Unique identifier for the schedule entry.
    arrival_time : datetime
        The time when a vehicle arrives at a specific stop.
    departure_time : datetime
        The time when a vehicle departs from a specific stop.
    direction_id : int
        The direction identifier for the route.
    drop_off_type : int
        The drop-off type for the stop (e.g., regular, no drop-off).
    pickup_type : int
        The pickup type for the stop (e.g., regular, no pickup).
    stop_headsign : str
        The headsign or destination displayed on the vehicle.
    stop_sequence : int
        The sequence number of the stop on the route.
    timepoint : bool
        Indicates if the stop is a timepoint (True) or not (False).
    route_id : str
        Identifier for the route associated with the schedule entry.
    stop_id : int
        Unique identifier for the stop.
    trip_id : int
        Unique identifier for the trip associated with the schedule entry.
    """

    __tablename__ = "schedule"

    event: str = db.Column(db.String(255), nullable=False)
    id: str = db.Column(db.String(255), primary_key=True, nullable=False)
    arrival_time = db.Column(db.TIMESTAMP)
    departure_time = db.Column(db.TIMESTAMP)
    direction_id: int = db.Column(db.Integer)
    drop_off_type: int = db.Column(db.Integer)
    pickup_type: int = db.Column(db.Integer)
    stop_headsign: str = db.Column(db.String(255))
    stop_sequence: int = db.Column(db.Integer)
    timepoint: bool = db.Column(db.Boolean)
    route_id: str = db.Column(db.String(255))
    stop_id: str = db.Column(db.String(255))
    trip_id: str = db.Column(db.String(255))
