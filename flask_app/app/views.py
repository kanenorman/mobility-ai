from flask import Blueprint, render_template

from .extensions import database as db
from .models import Schedule

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Index route for homepage."""
    schedule_data = db.session.query(Schedule).limit(10).all()
    return render_template("index.html", data=schedule_data)
