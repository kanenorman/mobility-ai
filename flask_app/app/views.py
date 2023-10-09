from flask import Blueprint, render_template

from .extensions import database as db
from .models import Route, Schedule, Shape, Stop, Trip

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Index route for homepage."""
    # Replace 'train_lines' with SQLAlchemy query
    train_lines_query = (
        db.session.query(Route.color, Shape.geometry)
        .join(Trip, Trip.route_id == Route.id)
        .join(Shape, Shape.id == Trip.shape_id)
        .all()
    )

    # Convert the result to GeoJSON format
    train_lines = [dict(color=row[0], geometry=row[1]) for row in train_lines_query]
    print(train_lines)

    stops = db.session.query(Stop).filter(Stop.parent_station.is_(None)).all()
    schedule_data = db.session.query(Schedule).limit(10).all()

    return render_template(
        "index.html", data=schedule_data, stops=stops, train_lines=train_lines
    )
