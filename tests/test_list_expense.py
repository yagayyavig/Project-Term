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

def test_list_expenses_sort_by_id(client, app):
    with app.app_context():
        cat = Category(name="ByID")
        db.session.add(cat)
        db.session.commit()
        db.session.add_all([
            Expense(amount=100, category=cat, note="First", date=datetime(2025, 1, 1)),
            Expense(amount=200, category=cat, note="Second", date=datetime(2025, 1, 2))
        ])
        db.session.commit()

    response = client.get("/expenses?sort=id")
    assert b"First" in response.data
    assert b"Second" in response.data


def test_list_expenses_sort_by_amount(client, app):
    with app.app_context():
        cat = Category(name="ByAmount")
        db.session.add(cat)
        db.session.commit()
        db.session.add_all([
            Expense(amount=5, category=cat, note="Cheap", date=datetime(2025, 1, 1)),
            Expense(amount=50, category=cat, note="Pricey", date=datetime(2025, 1, 2))
        ])
        db.session.commit()

    response = client.get("/expenses?sort=amount")
    assert b"Cheap" in response.data
    assert b"Pricey" in response.data


def test_list_expenses_sort_by_date(client, app):
    with app.app_context():
        cat = Category(name="ByDate")
        db.session.add(cat)
        db.session.commit()
        db.session.add_all([
            Expense(amount=10, category=cat, note="Old", date=datetime(2025, 1, 1)),
            Expense(amount=20, category=cat, note="New", date=datetime(2025, 2, 1))
        ])
        db.session.commit()

    response = client.get("/expenses?sort=date")
    assert b"Old" in response.data
    assert b"New" in response.data


def test_list_expenses_sort_by_category(client, app):
    with app.app_context():
        cat1 = Category(name="Alpha")
        cat2 = Category(name="Beta")
        db.session.add_all([cat1, cat2])
        db.session.commit()

        db.session.add_all([
            Expense(amount=10, category=cat1, note="A Expense", date=datetime(2025, 1, 1)),
            Expense(amount=20, category=cat2, note="B Expense", date=datetime(2025, 1, 2))
        ])
        db.session.commit()

    response = client.get("/expenses?sort=category")
    assert b"A Expense" in response.data
    assert b"B Expense" in response.data
