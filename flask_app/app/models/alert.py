from dataclasses import dataclass

from ..extensions import database as db


@dataclass
class Alert(db.Model):
    """
    Alert data model.

    Parameters
    ----------
    event : str
        Event identifier.
    id : str
        Unique identifier for the event data.
    active_period : str
        Active period information.
    banner : str
        Event banner information.
    cause : str
        Event cause information.
    created_at : datetime
        The timestamp when the event data was created.
    description : str
        Event description.
    effect : str
        Event effect information.
    header : str
        Event header information.
    image : str
        Event image information.
    image_alternative_text : str
        Alternative text for the event image.
    informed_entity : str
        Informed entity information.
    lifecycle : str
        Event lifecycle information.
    service_effect : str
        Service effect of the event.
    severity : str
        Event severity.
    short_header : str
        Short header for the event.
    timeframe : str
        Event timeframe information.
    updated_at : datetime
        The timestamp when the event data was last updated.
    type : str
        Event type.
    """

    __tablename__ = "alert"

    event: str = db.Column(db.String(255), nullable=False)
    id: str = db.Column(db.String(255), primary_key=True, nullable=False)
    active_period: str = db.Column(db.String(255), nullable=True)
    banner: str = db.Column(db.String(255))
    cause: str = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP)
    description: str = db.Column(db.String(255))
    effect: str = db.Column(db.String(255))
    header: str = db.Column(db.String(255))
    image: str = db.Column(db.String(255))
    image_alternative_text: str = db.Column(db.String(255))
    informed_entity: str = db.Column(db.String(255))
    lifecycle: str = db.Column(db.String(255))
    service_effect: str = db.Column(db.String(255))
    severity: str = db.Column(db.String(255))
    short_header: str = db.Column(db.String(255))
    timeframe: str = db.Column(db.String(255))
    updated_at: str = db.Column(db.TIMESTAMP)
    type: str = db.Column(db.String(255))
