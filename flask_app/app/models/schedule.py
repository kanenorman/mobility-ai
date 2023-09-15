from ..extensions import database as db


class Schedule(db.Model):
    __tablename__ = "schedule"

    id = db.Column(db.String(255), primary_key=True, nullable=False)
    arrival_time = db.Column(db.TIMESTAMP, nullable=True)
    departure_time = db.Column(db.TIMESTAMP, nullable=True)
    direction_id = db.Column(db.Integer, nullable=True)
    drop_off_type = db.Column(db.Integer, nullable=True)
    pickup_type = db.Column(db.Integer, nullable=True)
    stop_headsign = db.Column(db.String(255), nullable=True)
    stop_sequence = db.Column(db.Integer, nullable=True)
    timepoint = db.Column(db.Boolean, nullable=True)
    route_id = db.Column(db.String(255), nullable=True)
    stop_id = db.Column(db.Integer, nullable=True)
    trip_id = db.Column(db.Integer, nullable=True)

    def __init__(
        self,
        id,
        arrival_time,
        departure_time,
        direction_id,
        drop_off_type,
        pickup_type,
        stop_headsign,
        stop_sequence,
        timepoint,
        route_id,
        stop_id,
        trip_id,
    ):
        """
        Schedule entry for public transportation.

        Parameters
        ----------
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
        self.id = id
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.direction_id = direction_id
        self.drop_off_type = drop_off_type
        self.pickup_type = pickup_type
        self.stop_headsign = stop_headsign
        self.stop_sequence = stop_sequence
        self.timepoint = timepoint
        self.route_id = route_id
        self.stop_id = stop_id
        self.trip_id = trip_id
