import os

from flask import Flask

from .config import config
from .extensions import database
from .views import main


def create_app(app_environment="dev"):
    app = Flask(__name__)
    app.config.from_object(config[app_environment])
    app.register_blueprint(main)

    database.init_app(app)
    database.create_all()

    return app


if __name__ == "__main__":
    app = create_app(os.getenv("FLASK_ENV", "dev"))
    app.run()
