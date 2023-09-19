from ..extensions import database as db


class Alert(db.Model):
    __tablename__ = "alert"

    event = db.Column(db.String(255), nullable=False)
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    active_period = db.Column(db.String(255), nullable=True)
    banner = db.Column(db.String(255), nullable=True)
    cause = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=True)
    description = db.Column(db.String(255), nullable=True)
    effect = db.Column(db.String(255), nullable=True)
    header = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    image_alternative_text = db.Column(db.String(255), nullable=True)
    informed_entity = db.Column(db.String(255), nullable=True)
    lifecycle = db.Column(db.String(255), nullable=True)
    service_effect = db.Column(db.String(255), nullable=True)
    severity = db.Column(db.String(255), nullable=True)
    short_header = db.Column(db.String(255), nullable=True)
    timeframe = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.TIMESTAMP, nullable=True)
    type = db.Column(db.String(255), nullable=True)

    def __init__(
        self,
        event,
        id,
        active_period,
        banner,
        cause,
        created_at,
        description,
        effect,
        header,
        image,
        image_alternative_text,
        informed_entity,
        lifecycle,
        service_effect,
        severity,
        short_header,
        timeframe,
        updated_at,
        type,
    ):
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
        self.event = event
        self.id = id
        self.active_period = active_period
        self.banner = banner
        self.cause = cause
        self.created_at = created_at
        self.description = description
        self.effect = effect
        self.header = header
        self.image = image
        self.image_alternative_text = image_alternative_text
        self.informed_entity = informed_entity
        self.lifecycle = lifecycle
        self.service_effect = service_effect
        self.severity = severity
        self.short_header = short_header
        self.timeframe = timeframe
        self.updated_at = updated_at
        self.type = type
