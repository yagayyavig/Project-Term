import pytest
from app import app as flask_app, db

@pytest.fixture
def app():
    # Set up the Flask app in testing mode with in-memory SQLite
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with flask_app.app_context():
        from models import category, expense # Ensure all models are registered
        db.create_all()
        yield flask_app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()