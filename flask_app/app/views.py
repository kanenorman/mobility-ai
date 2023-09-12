from flask import Blueprint, render_template

from .models import Schedule

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Index route for homepage."""
    schedule_data = Schedule.query.all()
    return render_template("index.html", data=schedule_data)
