from dataclasses import dataclass

from ..extensions import database as db


@dataclass()
class Route(db.Model):
    """
    Route information for public transportation.

    Parameters
    ----------
    id : str
        Unique identifier for the route.
    event : str
        MBTA V3 API Streaming Event
    color : str
        The color associated with the route (e.g., "#FF0000").
    description : str
        A description of the route.
    direction_destinations : list
        A list of destination names for different directions.
    fare_class : str
        The fare class associated with the route.
    long_name : str
        The long name of the route.
    short_name : str
        The short name or code of the route.
    short_order : int
        The short order of the route.
    text_color : str
        The color of the text associated with the route (e.g., "#000000").
    type : int
        The type of the route.

    """

    __tablename__ = "route"

    id: str = db.Column(db.String(255), primary_key=True, nullable=False)
    event: str = db.Column(db.String(255), nullable=False)
    color: str = db.Column(db.String(7))
    description: str = db.Column(db.String(255))
    direction_destinations: list = db.Column(db.ARRAY(db.Text))
    fare_class: str = db.Column(db.String(255))
    long_name: str = db.Column(db.String(255))
    short_name: str = db.Column(db.String(255))
    short_order: int = db.Column(db.Integer)
    text_color: str = db.Column(db.String(7))
    type: int = db.Column(db.Integer)
