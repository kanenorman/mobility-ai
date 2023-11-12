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
    id : str
        Unique identifier for the stop entry.
    name : str
        Name associated with the stop.
    type : str
        Type of the stop entry.
    event : str
        MBTA V3 API Streaming Event.
    address : str
        The address of the stop.
    at_street : str
        The street at which the stop is located.
    on_street : str
        The street on which the stop is located.
    municipality : str
        The municipality where the stop is located.
    latitude : float
        Latitude coordinate of the stop location.
    longitude : float
        Longitude coordinate of the stop location.
    parent_station_id : str
        Identifier for the parent station, if applicable.
    parent_station_type : str
        Type of the parent station, if applicable.
    parent_station : str
        Identifier for the parent station, if applicable.
    location_type : str
        The type of location (e.g., platform, station).
    zone_id : str
        Zone information for the stop.
    platform_code : str
        Code associated with the platform.
    platform_name : str
        Name of the platform.
    vehicle_type : str
        Type of vehicle associated with the stop.
    wheelchair_boarding : int
        Indicates if wheelchair boarding is available.
    facilities_self : str
        Facilities information for the stop.
    description : str
        Description of the stop.
    self : str
        Self information for the stop.

    Notes
    -----
    - The `id` field is a unique identifier for the stop entry.
    - The `event` field represents the MBTA V3 API Streaming Event.
    - The `location_type` field indicates the type of location (e.g., platform, station).
    - The `wheelchair_boarding` field indicates if wheelchair boarding is available.
    - The `zone_id` field contains zone information for the stop.
    - The `parent_station` field is used to identify the parent station, if applicable.
    """

    __tablename__ = "stop"

    id: str = db.Column(db.String(255), primary_key=True, nullable=False)
    name: str = db.Column(db.String(255), nullable=True)
    type: str = db.Column(db.String(255), nullable=True)
    event: str = db.Column(db.String(255), nullable=True)
    address: str = db.Column(db.String(255), nullable=True)
    at_street: str = db.Column(db.String(255), nullable=True)
    on_street: str = db.Column(db.String(255), nullable=True)
    municipality: str = db.Column(db.String(255), nullable=True)
    latitude: float = db.Column(db.Float, nullable=True)
    longitude: float = db.Column(db.Float, nullable=True)
    parent_station_id: str = db.Column(db.String(255), nullable=True)
    parent_station_type: str = db.Column(db.String(255), nullable=True)
    parent_station: str = db.Column(db.String(255), nullable=True)
    location_type: str = db.Column(db.String(255), nullable=True)
    zone_id: str = db.Column(db.String(255), nullable=True)
    platform_code: str = db.Column(db.String(255), nullable=True)
    platform_name: str = db.Column(db.String(255), nullable=True)
    vehicle_type: str = db.Column(db.String(255), nullable=True)
    wheelchair_boarding: int = db.Column(db.Integer, nullable=True)
    facilities_self: str = db.Column(db.String(255), nullable=True)
    description: str = db.Column(db.String(255), nullable=True)
    self: str = db.Column(db.String(255), nullable=True)
