from db import db
from models.expense import Expense
from models.category import Category
from datetime import datetime

def test_list_expenses(client, app):
    with app.app_context():
        category = Category(name="Test Category")
        db.session.add(category)
        db.session.commit()

        expense = Expense(
            amount=50.0,
            category=category,
            note="Sample",
            date=datetime(2025, 1, 1)
        )
        db.session.add(expense)
        db.session.commit()

    response = client.get("/expenses")
    assert response.status_code == 200
    assert b"Expenses" in response.data or b"Add Expense" in response.data
    assert b"Sample" in response.data  # ✅ confirm expense shows up
