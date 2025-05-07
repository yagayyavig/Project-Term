from db import db
from sqlalchemy import DateTime


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.mapped_column(db.Integer, primary_key=True)
    amount = db.mapped_column(db.Float, nullable=False)
    category = db.mapped_column(db.String, nullable=False)
    date = db.mapped_column(DateTime, nullable=False)
    note = db.mapped_column(db.String)

