from db import db
from sqlalchemy import DateTime, Nullable 

class Category(db.Model):
    __tablename__ = "categories"

    id = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String, nullable=False, unique=True)

    expenses = db.relationship("Expenses", back_populates="category")