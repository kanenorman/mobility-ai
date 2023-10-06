from flask import Blueprint, render_template
from geoalchemy2 import functions

from .extensions import database as db
from .models import Schedule, Shape, Stop

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Index route for homepage."""
    train_lines = db.session.scalar(functions.ST_AsGeoJSON(Shape.geometry))
    stops = db.session.query(Stop).filter(Stop.parent_station.is_(None)).all()
    schedule_data = db.session.query(Schedule).limit(10).all()

    return render_template(
        "index.html", data=schedule_data, stops=stops, train_lines=train_lines
    )
