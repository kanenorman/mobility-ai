from dataclasses import dataclass

from ..extensions import database as db


@dataclass()
class Trip(db.Model):
    """
    Trip entry for public transportation.

    A Trip is defined as the journey of a particular vehicle
    through a set of stops on a primary route.

    Parameters
    ----------
    event : str
        MBTA V3 API Streaming Event
    id : str
        Unique identifier for the trip entry.
    type : str
        Type of the trip entry.
    bikes_allowed : int
        Indicates if bikes are allowed on the trip.
    block_id : str
        Identifier for the block associated with the trip.
    direction_id : int
        The direction identifier for the trip.
    headsign : str
        The headsign or destination displayed on the vehicle.
    name : str
        Name associated with the trip.
    wheelchair_accessible : int
        Indicates if the trip is wheelchair accessible.
    shape_id : str
        Identifier for the shape associated with the trip.
    service_id : str
        Identifier for the service associated with the trip.
    route_id : str
        Identifier for the route associated with the trip.
    route_pattern_id : str
        Identifier for the route pattern associated with the trip.
    """

    __tablename__ = "trip"

    event: str = db.Column(db.String(255), nullable=False)
    id: str = db.Column(db.String(255), primary_key=True, nullable=False)
    type: str = db.Column(db.String(255), nullable=False)
    bikes_allowed: int = db.Column(db.Integer)
    block_id: str = db.Column(db.String(255))
    direction_id: int = db.Column(db.Integer)
    headsign: str = db.Column(db.String(255))
    name: str = db.Column(db.String(255))
    wheelchair_accessible: int = db.Column(db.Integer)
    shape_id: str = db.Column(db.String(255))
    service_id: str = db.Column(db.String(255))
    route_id: str = db.Column(db.String(255))
    route_pattern_id: str = db.Column(db.String(255))
