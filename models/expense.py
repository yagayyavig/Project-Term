from db import db
from sqlalchemy import Date


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.mapped_column(db.Integer, primary_key=True)
    amount = db.mapped_column(db.Float, nullable=False)
    category = db.mapped_column(db.String, nullable=False)
    date = db.mapped_column(Date, nullable=False)
    note = db.mapped_column(db.String)

    # Category foreign key and relationship
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", back_populates="expenses")

    def __repr__(self):
        return f"<Expense {self.amount} on {self.date}>"