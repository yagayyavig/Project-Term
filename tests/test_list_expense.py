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

def test_list_expenses_empty(client):
    response = client.get("/expenses")
    assert response.status_code == 200
    assert b"No expenses" in response.data or b"Add Expense" in response.data

def test_list_expenses_multiple(client, app):
    with app.app_context():
        cat = Category(name="Food")
        db.session.add(cat)
        db.session.commit()

        db.session.add_all([
            Expense(amount=10, category=cat, note="Milk", date=datetime(2025, 1, 2)),
            Expense(amount=15, category=cat, note="Bread", date=datetime(2025, 1, 1))
        ])
        db.session.commit()

    response = client.get("/expenses")
    assert b"Milk" in response.data
    assert b"Bread" in response.data

def test_invalid_route(client):
    response = client.get("/expenses/invalid")
    assert response.status_code in (404, 302)
