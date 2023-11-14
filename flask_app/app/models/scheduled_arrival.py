from dataclasses import dataclass
from datetime import datetime
from typing import List

from sqlalchemy.dialects import postgresql

from ..extensions import database as db


@dataclass
class ScheduledArrival(db.Model):
    __tablename__ = "scheduled_arrival"

    route_id: str = db.Column(db.String(255), nullable=True)
    stop_name: str = db.Column(db.String(255), nullable=True, primary_key=True)
    direction_id: int = db.Column(db.Integer, nullable=True, primary_key=True)
    stop_sequence: int = db.Column(db.Integer, nullable=True)
    arrival_times: List[datetime] = db.Column(
        postgresql.ARRAY(postgresql.TIMESTAMP), nullable=True
    )
