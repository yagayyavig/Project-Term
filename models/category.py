from db import db

class Category(db.Model):
    __tablename__="category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Reference to Expenses
    expenses = db.relationship("Expense", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"