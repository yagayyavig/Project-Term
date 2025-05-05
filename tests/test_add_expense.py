from db import db
from models.category import Category
from datetime import datetime, timedelta

def create_category(name="Food"):
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return category

def test_add_expense_get(client):
    response = client.get("/expenses/add")
    assert response.status_code == 200
    assert b"Add Expense" in response.data or b"amount" in response.data

def test_add_expense_future_date(client, app):
    with app.app_context():
        category = create_category("Travel")
        future_date = (datetime.today() + timedelta(days=5)).strftime("%Y-%m-%d")
        response = client.post("/expenses/add", data={
            "amount": "100",
            "category_id": str(category.id),  # FIXED
            "date": future_date,
            "note": "Testing future"
        })
        assert response.status_code == 200
        assert b"Cannot add expense for a future date!" in response.data

def test_add_expense_valid(client, app):
    with app.app_context():
        category = create_category("Food")
        today = datetime.today().strftime("%Y-%m-%d")
        response = client.post("/expenses/add", data={
            "amount": "75.5",
            "category_id": str(category.id),  # FIXED
            "date": today,
            "note": "Test lunch"
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b"Test lunch" in response.data
