from db import db
from models.expense import Expense
from models.category import Category
from datetime import datetime


def test_expenses_by_category(client, app):
    with app.app_context():
        cat = Category(name="Transport")
        db.session.add(cat)
        db.session.commit()

        expense = Expense(amount=20.0, category=cat, note="Bus", date=datetime(2025, 1, 1))
        db.session.add(expense)
        db.session.commit()
        cat_id = cat.id

    response = client.get(f"/expenses/category/{cat_id}")
    assert response.status_code == 200
    assert b"Bus" in response.data
    assert b"Transport" in response.data

def test_expenses_by_category_invalid(client):
    response = client.get("/expenses/category/99999")
    assert response.status_code == 200
    assert b"Category not found" in response.data


def test_expenses_by_category_sort(client, app):
    with app.app_context():
        cat = Category(name="SortedCat")
        db.session.add(cat)
        db.session.commit()

        db.session.add_all([
            Expense(amount=100, category=cat, note="Big", date=datetime(2025, 1, 2)),
            Expense(amount=10, category=cat, note="Small", date=datetime(2025, 1, 1))
        ])
        db.session.commit()
        cat_id = cat.id  # ✅ store while still in context

    response = client.get(f"/expenses/category/{cat_id}?sort=amount")
    assert response.status_code == 200
    assert b"Big" in response.data
    assert b"Small" in response.data


def test_expenses_by_category_sort_id(client, app):
    with app.app_context():
        cat = Category(name="SortID")
        db.session.add(cat)
        db.session.commit()

        db.session.add_all([
            Expense(amount=50, category=cat, note="First", date=datetime(2025, 1, 1)),
            Expense(amount=75, category=cat, note="Second", date=datetime(2025, 1, 2))
        ])
        db.session.commit()
        cat_id = cat.id

    response = client.get(f"/expenses/category/{cat_id}?sort=id")
    assert b"First" in response.data
    assert b"Second" in response.data


def test_expenses_by_category_sort_date(client, app):
    with app.app_context():
        cat = Category(name="SortDate")
        db.session.add(cat)
        db.session.commit()

        db.session.add_all([
            Expense(amount=30, category=cat, note="Earlier", date=datetime(2025, 1, 1)),
            Expense(amount=40, category=cat, note="Later", date=datetime(2025, 1, 3))
        ])
        db.session.commit()
        cat_id = cat.id

    response = client.get(f"/expenses/category/{cat_id}?sort=date")
    assert b"Earlier" in response.data
    assert b"Later" in response.data
