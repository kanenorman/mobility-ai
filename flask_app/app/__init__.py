import os

from flask import Flask

from .config import config
from .extensions import database
from .views import main


def create_app() -> Flask:
    """
    Entry point for creating flask app.

    Returns
    -------
    Flask
        flask app
    """
    app_environment = os.getenv("FLASK_ENV") or "dev"

    app = Flask(__name__)
    app.config.from_object(config[app_environment])
    app.register_blueprint(main)

    with app.app_context():
        database.init_app(app)
        database.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
