from ..extensions import database as db


class Stop(db.Model):
    __tablename__ = "stop"

    event = db.Column(db.String(255), nullable=False)
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    at_street = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    location_type = db.Column(db.Integer, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    municipality = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    on_street = db.Column(db.String(255), nullable=True)
    platform_code = db.Column(db.String(255), nullable=True)
    platform_name = db.Column(db.String(255), nullable=True)
    vehicle_type = db.Column(db.String(255), nullable=True)
    wheelchair_boarding = db.Column(db.Integer, nullable=True)
    zone = db.Column(db.String(255), nullable=True)
    parent_station = db.Column(db.String(255), nullable=True)

    def __init__(
        self,
        event,
        id,
        type,
        address,
        at_street,
        description,
        latitude,
        location_type,
        longitude,
        municipality,
        name,
        on_street,
        platform_code,
        platform_name,
        vehicle_type,
        wheelchair_boarding,
        zone,
        parent_station,
    ):
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
        self.event = event
        self.id = id
        self.type = type
        self.address = address
        self.at_street = at_street
        self.description = description
        self.latitude = latitude
        self.location_type = location_type
        self.longitude = longitude
        self.municipality = municipality
        self.name = name
        self.on_street = on_street
        self.platform_code = platform_code
        self.platform_name = platform_name
        self.vehicle_type = vehicle_type
        self.wheelchair_boarding = wheelchair_boarding
        self.zone = zone
        self.parent_station = parent_station
