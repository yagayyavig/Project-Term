from db import db
from sqlalchemy import DateTime
from models.category import Category  # needed if using class-based relationship

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.mapped_column(db.Integer, primary_key=True)
    amount = db.mapped_column(db.Float, nullable=False)
    date = db.mapped_column(DateTime, nullable=False)
    note = db.mapped_column(db.String)

    category_id = db.mapped_column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship(Category, back_populates="expenses")  # relationship to Category
