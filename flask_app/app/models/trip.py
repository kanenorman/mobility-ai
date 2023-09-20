from ..extensions import database as db


class Trip(db.Model):
    __tablename__ = "trip"

    event = db.Column(db.String(255), nullable=False)
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    bikes_allowed = db.Column(db.Integer, nullable=True)
    block_id = db.Column(db.String(255), nullable=True)
    direction_id = db.Column(db.Integer, nullable=True)
    headsign = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    wheelchair_accessible = db.Column(db.Integer, nullable=True)
    shape_id = db.Column(db.String(255), nullable=True)
    service_id = db.Column(db.String(255), nullable=True)
    route_id = db.Column(db.String(255), nullable=True)
    route_pattern_id = db.Column(db.String(255), nullable=True)

    def __init__(
        self,
        event,
        id,
        type,
        bikes_allowed,
        block_id,
        direction_id,
        headsign,
        name,
        wheelchair_accessible,
        shape_id,
        service_id,
        route_id,
        route_pattern_id,
    ):
        """
        Trip entry for public transportation.

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
        self.event = event
        self.id = id
        self.type = type
        self.bikes_allowed = bikes_allowed
        self.block_id = block_id
        self.direction_id = direction_id
        self.headsign = headsign
        self.name = name
        self.wheelchair_accessible = wheelchair_accessible
        self.shape_id = shape_id
        self.service_id = service_id
        self.route_id = route_id
        self.route_pattern_id = route_pattern_id
