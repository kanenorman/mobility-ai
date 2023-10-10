from flask import Blueprint, render_template
from geoalchemy2.functions import ST_AsGeoJSON, ST_Collect

from .extensions import database as db
from .models import Route, Schedule, Shape, Stop, Trip

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Index route for homepage."""
    train_lines = (
        db.session.query(Route.color, ST_AsGeoJSON(ST_Collect(Shape.geometry)))
        .join(Trip, Trip.route_id == Route.id)
        .join(Shape, Shape.id == Trip.shape_id)
        .group_by(Route.color)
        .all()
    )

    train_lines = [(color, geometry) for color, geometry in train_lines]
    stops = db.session.query(Stop).filter(Stop.parent_station.is_(None)).all()
    schedule_data = db.session.query(Schedule).limit(10).all()

    return render_template(
        "index.html",
        data=schedule_data,
        stops=stops,
        train_lines=train_lines,
    )
