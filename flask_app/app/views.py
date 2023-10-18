import os

from flask import Blueprint, render_template

from .extensions import database as db
from .models import Schedule, Stop

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Index route for homepage."""
    stops = db.session.query(Stop).filter(Stop.parent_station.is_(None)).all()
    schedule_data = db.session.query(Schedule).limit(10).all()
    # TODO: Setup Token Management Before Production
    mapbox_token = os.environ["MAPBOX_TOKEN"]
    return render_template(
        "index.html", data=schedule_data, stops=stops, mapbox_token=mapbox_token
    )


@main.route("/terms/")
def terms():
    """Terms and Conditions for Usage."""
    return render_template("terms.html")


@main.route("/copyright/")
def copyright():
    """Copyright Notice."""
    return render_template("copyright.html")


@main.route("/about/")
def about():
    """About Us."""
    return render_template("about.html")
