import os
from datetime import datetime
from typing import List, Tuple

from flask import Blueprint, render_template
from sqlalchemy.orm import Query

from .extensions import database as db
from .models import Location, ScheduledArrival

main = Blueprint("main", __name__)


def _get_train_schedule(route: str) -> List[Tuple[str, List[datetime]]]:
    """
    Get train schedules for a specific route.

    Parameters
    ----------
    route : str
        Valid MBTA route name (e.g `Red`, `Blue`, `Green-B`, `Green-B`, `Green-C`)

    Returns
    -------
    List[Tuple[str, List[datetime]]]
        List of tuples containing the train stop name and scheduled arrival times.
        Sort order is gaurenteed.
    """
    query: Query = (
        db.session.query(
            ScheduledArrival.stop_name,
            ScheduledArrival.arrival_times,
        )
        .filter(ScheduledArrival.route_id == route)
        .all()
    )

    return query


@main.route("/")
def index():
    """Index route for homepage."""
    mapbox_token = os.environ["MAPBOX_TOKEN"]

    stops = db.session.query(Location).all()
    red_schedule = _get_train_schedule("Red")
    blue_schedule = _get_train_schedule("Blue")
    orange_schedule = _get_train_schedule("Orange")
    green_b_schedule = _get_train_schedule("Green-B")
    green_c_schedule = _get_train_schedule("Green-C")
    green_d_schedule = _get_train_schedule("Green-C")

    return render_template(
        "index.html",
        red_schedule=red_schedule,
        blue_schedule=blue_schedule,
        orange_schedule=orange_schedule,
        green_b_schedule=green_b_schedule,
        green_c_schedule=green_c_schedule,
        green_d_schedule=green_d_schedule,
        stops=stops,
        mapbox_token=mapbox_token,
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
