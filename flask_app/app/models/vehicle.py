from dataclasses import dataclass

from ..extensions import database as db


@dataclass()
class Vehicle(db.Model):
    """
    Represents a vehicle in a transportation system.

    Parameters
    ----------
    event : str
        The event associated with the SSE.
    id : str
        The unique identifier of the vehicle.
    type : str
        The type of the vehicle.
    bearing : int
        The bearing of the vehicle.
    current_status : str
        The current status of the vehicle.
    current_stop_sequence : int
        The current stop sequence of the vehicle.
    direction_id : int
        The direction ID of the vehicle.
    label : int
        The label of the vehicle.
    latitude : float
        The latitude coordinate of the vehicle's location.
    longitude : float
        The longitude coordinate of the vehicle's location.
    occupancy_status : str
        The occupancy status of the vehicle.
    speed : int
        The speed of the vehicle.
    updated_at : int
        The timestamp of the last update for the vehicle.
    route_id : str, optional
        The route ID associated with the vehicle.
    stop_id : str, optional
        The stop ID associated with the vehicle.
    trip_id : str, optional
        The trip ID associated with the vehicle.

    See Also
    --------
    https://api-v3.mbta.com/docs/swagger/index.html#/Vehicle/ : Official swagger docs
    """

    __tablename__ = "vehicle"

    event: str = db.Column(db.String(255), nullable=False)
    id: str = db.Column(db.String(255), nullable=False)
    type: str = db.Column(db.String(255))
    bearing: int = db.Column(db.Integer)
    current_status: str = db.Column(db.String(255))
    current_stop_sequence: int = db.Column(db.Integer)
    direction_id: int = db.Column(db.Integer)
    label: int = db.Column(db.String(255))
    latitude: float = db.Column(db.Double)
    longitude: float = db.Column(db.Double)
    occupancy_status: float = db.Column(db.String(255))
    speed: int = db.Column(db.Integer)
    updated_at: int = db.Column(db.TIMESTAMP, nullable=False)
    route_id: str = db.Column(db.String(255))
    stop_id: str = db.Column(db.String(255))
    trip_id: str = db.Column(db.String(255))
