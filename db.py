from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def setup_db(app):
    """Initializes and creates the database."""
    db.init_app(app)
    with app.app_context():
        db.create_all()