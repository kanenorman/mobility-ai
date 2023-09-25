from dataclasses import dataclass

from ..extensions import database as db


@dataclass(slots=True)
class Vehicle(db.Model):
    __tablename__ = "vehicle"

    event: str = db.Column(db.String(255), nullable=False)
    id: str = db.Column(db.String(255), primary_key=True, nullable=False)
    type: str = db.Column(db.String(255))
    bearing: int = db.Column(db.Integer)
    current_status: str = db.Column(db.String(255))
    current_stop_sequence: int = db.Column(db.Integer)
    direction_id: int = db.Column(db.Integer)
    label: int = db.Column(db.Integer)
    latitude: float = db.Column(db.Double)
    longitude: float = db.Column(db.Double)
    occupancy_status: float = db.Column(db.Double)
    speed: int = db.Column(db.Integer)
    updated_at: int = db.Column(db.TIMESTAMP)
    route_id: str = db.Column(db.String(255), nullable=True)
    stop_id: str = db.Column(db.String(255), nullable=True)
    trip_id: str = db.Column(db.String(255), nullable=True)
