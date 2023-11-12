from dataclasses import dataclass
from datetime import datetime

from ..extensions import database as db


@dataclass
class Vehicle(db.Model):
    """
    Vehicle entry for public transportation.

    A Vehicle represents a vehicle used for public transportation.

    Parameters
    ----------
    id : str
        Unique identifier for the vehicle entry.
    label : str
        Label associated with the vehicle.
    type : str
        Type of the vehicle.
    event : str
        MBTA V3 API Streaming Event.
    route_type : str
        Type of the route associated with the vehicle.
    stop_id : str
        Identifier for the stop associated with the vehicle.
    stop_type : str
        Type of the stop associated with the vehicle.
    trip_id : str
        Identifier for the trip associated with the vehicle.
    trip_type : str
        Type of the trip associated with the vehicle.
    bearing : int
        Bearing information for the vehicle.
    current_status : str
        Current status of the vehicle.
    current_stop_sequence : int
        Current stop sequence for the vehicle.
    direction_id : int
        Direction identifier for the vehicle.
    latitude : float
        Latitude coordinate of the vehicle's location.
    longitude : float
        Longitude coordinate of the vehicle's location.
    speed : float
        Speed of the vehicle.
    updated_at : datetime
        Timestamp indicating when the vehicle information was last updated.
    self : str
        Self information for the vehicle.

    Notes
    -----
    - The `id` field is a unique identifier for the vehicle entry.
    - The `event` field represents the MBTA V3 API Streaming Event.
    - The `bearing` field provides bearing information for the vehicle.
    - The `current_status` field indicates the current status of the vehicle.
    - The `current_stop_sequence` field represents the current stop sequence for the vehicle.
    - The `direction_id` field is used to identify the direction of the vehicle.
    - The `latitude` and `longitude` fields specify the vehicle's location coordinates.
    - The `speed` field represents the speed of the vehicle.
    - The `updated_at` field indicates when the vehicle information was last updated.
    """

    __tablename__ = "vehicle"

    id: str = db.Column(db.String(255), primary_key=True, nullable=False)
    label: str = db.Column(db.String(255), nullable=True)
    type: str = db.Column(db.String(255), nullable=True)
    event: str = db.Column(db.String(255), nullable=True)
    route_type: str = db.Column(db.String(255), nullable=True)
    stop_id: str = db.Column(db.String(255), nullable=True)
    stop_type: str = db.Column(db.String(255), nullable=True)
    trip_id: str = db.Column(db.String(255), nullable=True)
    trip_type: str = db.Column(db.String(255), nullable=True)
    bearing: int = db.Column(db.Integer, nullable=True)
    current_status: str = db.Column(db.String(255), nullable=True)
    current_stop_sequence: int = db.Column(db.Integer, nullable=True)
    direction_id: int = db.Column(db.Integer, nullable=True)
    latitude: float = db.Column(db.Float, nullable=True)
    longitude: float = db.Column(db.Float, nullable=True)
    speed: float = db.Column(db.Float, nullable=True)
    updated_at: datetime = db.Column(db.TIMESTAMP, nullable=True)
    self: str = db.Column(db.String(255), nullable=True)
