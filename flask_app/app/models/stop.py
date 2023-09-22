from dataclasses import dataclass

from ..extensions import database as db


@dataclass
class Stop(db.Model):
    """
    Stop entry for public transportation.

    A Stop is defined as a location where vehicles stop to pick up
    or drop off passengers.

    Parameters
    ----------
    event : str
        MBTA V3 API Streaming Event
    id : str
        Unique identifier for the stop entry.
    type : str
        Type of the stop entry.
    address : str
        The address of the stop.
    at_street : str
        The street at which the stop is located.
    description : str
        Description of the stop.
    latitude : float
        Latitude coordinate of the stop location.
    location_type : int
        The type of location (e.g., platform, station).
    longitude : float
        Longitude coordinate of the stop location.
    municipality : str
        The municipality where the stop is located.
    name : str
        Name associated with the stop.
    on_street : str
        The street on which the stop is located.
    platform_code : str
        Code associated with the platform.
    platform_name : str
        Name of the platform.
    vehicle_type : str
        Type of vehicle associated with the stop.
    wheelchair_boarding : int
        Indicates if wheelchair boarding is available.
    zone : str
        Zone information for the stop.
    parent_station : str
        Identifier for the parent station, if applicable.
    """

    __tablename__ = "stop"

    event: str = db.Column(db.String(255), nullable=False)
    id: str = db.Column(db.String(255), primary_key=True, nullable=False)
    type: str = db.Column(db.String(255), nullable=False)
    address: str = db.Column(db.String(255), nullable=True)
    at_street: str = db.Column(db.String(255), nullable=True)
    description: str = db.Column(db.String(255), nullable=True)
    latitude: float = db.Column(db.Float, nullable=True)
    location_type: int = db.Column(db.Integer, nullable=True)
    longitude: float = db.Column(db.Float, nullable=True)
    municipality: str = db.Column(db.String(255), nullable=True)
    name: str = db.Column(db.String(255), nullable=True)
    on_street: str = db.Column(db.String(255), nullable=True)
    platform_code: str = db.Column(db.String(255), nullable=True)
    platform_name: str = db.Column(db.String(255), nullable=True)
    vehicle_type: str = db.Column(db.String(255), nullable=True)
    wheelchair_boarding: int = db.Column(db.Integer, nullable=True)
    zone: str = db.Column(db.String(255), nullable=True)
    parent_station: str = db.Column(db.String(255), nullable=True)
