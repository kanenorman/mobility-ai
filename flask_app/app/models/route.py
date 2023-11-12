from dataclasses import dataclass
from typing import List

from sqlalchemy.dialects import postgresql

from ..extensions import database as db


@dataclass
class Route(db.Model):
    """
    Route entry for public transportation.

    A Route represents a public transportation route.

    Parameters
    ----------
    id : str
        Unique identifier for the route entry.
    long_name : str
        Long name associated with the route.
    short_name : str
        Short name associated with the route.
    type : int
        Type of the route.
    event : str
        MBTA V3 API Streaming Event.
    color : str
        Color code associated with the route.
    text_color : str
        Text color code associated with the route.
    description : str
        Description of the route.
    direction_destinations : List[str]
        List of direction destinations for the route.
    direction_names : List[str]
        List of direction names for the route.
    fare_class : str
        Fare class associated with the route.
    short_order : int
        Short order number for the route.
    line_id : str
        Identifier for the line associated with the route.
    line_type : str
        Type of the line associated with the route.
    self : str
        Self information for the route.

    Notes
    -----
    - The `id` field is a unique identifier for the route entry.
    - The `event` field represents the MBTA V3 API Streaming Event.
    - The `type` field specifies the type of the route.
    - The `direction_destinations` field contains a list of direction destinations.
    - The `direction_names` field contains a list of direction names.
    - The `short_order` field represents the short order number for the route.
    """

    __tablename__ = "route"

    id: str = db.Column(db.String(255), primary_key=True, nullable=False)
    long_name: str = db.Column(db.String(255), nullable=True)
    short_name: str = db.Column(db.String(255), nullable=True)
    type: int = db.Column(db.Integer, nullable=True)
    event: str = db.Column(db.String(255), nullable=True)
    color: str = db.Column(db.String(7), nullable=True)
    text_color: str = db.Column(db.String(7), nullable=True)
    description: str = db.Column(db.String(255), nullable=True)
    direction_destinations: List[str] = db.Column(
        postgresql.ARRAY(db.String), nullable=True
    )
    direction_names: List[str] = db.Column(postgresql.ARRAY(db.String), nullable=True)
    fare_class: str = db.Column(db.String(255), nullable=True)
    short_order: int = db.Column(db.Integer, nullable=True)
    line_id: str = db.Column(db.String(255), nullable=True)
    line_type: str = db.Column(db.String(255), nullable=True)
    self: str = db.Column(db.String(255), nullable=True)
