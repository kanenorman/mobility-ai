from dataclasses import dataclass

from geoalchemy2 import Geometry

from ..extensions import database as db


@dataclass
class Shape(db.Model):
    """
    Shape entry for public transportation.

    A Stop is defined as a location where vehicles stop to pick up
    or drop off passengers.

    Parameters
    ----------
    event : str
        MBTA V3 API Streaming Event.
    id : str
        Unique identifier for the shape entry.
    type : str
        Type of the entry.
    geometry :
        Geographical representation of geometric shape.
    """

    __tablename__ = "shape"

    event: str = db.Column(db.String(255), nullable=False)
    id: str = db.Column(db.String(255), primary_key=True, nullable=False)
    type: str = db.Column(db.String(255), nullable=False)
    geometry: str = db.Column(Geometry("LINESTRING"))
