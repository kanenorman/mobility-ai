from dataclasses import dataclass

from ..extensions import database as db


@dataclass()
class Location(db.Model):
    __tablename__ = "location"
    stop_name: str = db.Column(db.String(255), primary_key=True, nullable=False)
    longitude: float = db.Column(db.Float(), nullable=False)
    latitude: float = db.Column(db.Float(), nullable=False)
    color: str = db.Column(db.String(255), nullable=False)
