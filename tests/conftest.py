import pytest
from app import create_app, db

@pytest.fixture
def app():
    # Set up the Flask app in testing mode with in-memory SQLite
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        from models import category, expense # Ensure all models are registered
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()