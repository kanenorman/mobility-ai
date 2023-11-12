from dataclasses import dataclass
from datetime import datetime

from ..extensions import database as db


@dataclass
class Schedule(db.Model):
    """
    Schedule entry for public transportation.

    A Schedule represents schedule information for public transportation trips.

    Parameters
    ----------
    id : str
        Unique identifier for the schedule entry.
    type : str
        Type of the schedule entry.
    event : str
        MBTA V3 API Streaming Event.
    trip_id : str
        Identifier for the trip associated with the schedule.
    trip_type : str
        Type of the trip associated with the schedule.
    route_id : str
        Identifier for the route associated with the schedule.
    route_type : str
        Type of the route associated with the schedule.
    stop_id : str
        Identifier for the stop associated with the schedule.
    stop_type : str
        Type of the stop associated with the schedule.
    arrival_time : datetime
        Arrival time for the schedule.
    departure_time : datetime
        Departure time for the schedule.
    direction_id : int
        Direction identifier for the schedule.
    stop_headsign : str
        Stop headsign information for the schedule.
    stop_sequence : int
        Stop sequence number for the schedule.
    pickup_type : int
        Pickup type information for the schedule.
    drop_off_type : int
        Drop-off type information for the schedule.
    timepoint : bool
        Indicates if the schedule represents a timepoint.

    Notes
    -----
    - The `id` field is a unique identifier for the schedule entry.
    - The `event` field represents the MBTA V3 API Streaming Event.
    - The `arrival_time` and `departure_time` fields represent schedule times.
    - The `direction_id` field is used to identify the direction of the schedule.
    - The `timepoint` field indicates whether the schedule represents a timepoint.
    """

    __tablename__ = "schedule"

    id: str = db.Column(db.String(255), primary_key=True, nullable=False)
    type: str = db.Column(db.String(255), nullable=True)
    event: str = db.Column(db.String(255), nullable=True)
    trip_id: str = db.Column(db.String(255), nullable=True)
    trip_type: str = db.Column(db.String(255), nullable=True)
    route_id: str = db.Column(db.String(255), nullable=True)
    route_type: str = db.Column(db.String(255), nullable=True)
    stop_id: str = db.Column(db.String(255), nullable=True)
    stop_type: str = db.Column(db.String(255), nullable=True)
    arrival_time: datetime = db.Column(db.TIMESTAMP, nullable=True)
    departure_time: datetime = db.Column(db.TIMESTAMP, nullable=True)
    direction_id: int = db.Column(db.Integer, nullable=True)
    stop_headsign: str = db.Column(db.String(255), nullable=True)
    stop_sequence: int = db.Column(db.Integer, nullable=True)
    pickup_type: int = db.Column(db.Integer, nullable=True)
    drop_off_type: int = db.Column(db.Integer, nullable=True)
    timepoint: bool = db.Column(db.Boolean, nullable=True)
