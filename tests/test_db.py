from flask import Flask
from db import db, setup_db

def test_setup_db_direct():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    setup_db(app)
    assert "sqlalchemy" in app.extensions
