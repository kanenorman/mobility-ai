from .extensions import database as db


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
