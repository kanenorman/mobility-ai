from datetime import datetime

import pytest
from flask import Flask

from flask_app.app import main
from flask_app.app.extensions import database as db


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.register_blueprint(main)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_get_train_schedule(monkeypatch):
    """
    Mock Arrivals and Preditctions
    """

    def mock_query(route):
        return [
            ("Stop1", [datetime(2023, 1, 1, 10, 0, 0), datetime(2023, 1, 1, 12, 0, 0)])
        ]

    monkeypatch.setattr(main, "_get_train_schedule", mock_query)
