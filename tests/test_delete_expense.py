from db import db
from models.expense import Expense
from models.category import Category
from datetime import datetime

def create_category(name="Dont matter"):
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return category

# test the confirm delete actually deletes
def test_confirm_delete_button(client, app):
    with app.app_context():
        category = create_category()
        expense = Expense(
            amount=10.0,
            category=category,  
            note="Test",
            date=datetime(2025, 1, 1)
        )
        db.session.add(expense)
        db.session.commit()
        expense_id = expense.id

    response = client.get(f"/expenses/{expense_id}/deleteconfirm")
    assert response.status_code == 200
    assert b"Confirm Deletion" in response.data

    response = client.post(f"/expenses/{expense_id}/delete", follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        deleted = db.session.get(Expense, expense_id)
        assert deleted is None

# test the cancel does nothing
def test_cancel_button(client, app):
    with app.app_context():
        category = create_category()
        expense = Expense(
            amount=10.0,
            category=category,  
            note="Test",
            date=datetime(2025, 1, 1)
        )
        db.session.add(expense)
        db.session.commit()
        expense_id = expense.id

    response = client.get(f"/expenses/{expense_id}/deleteconfirm")
    assert response.status_code == 200
    assert b"Cancel" in response.data

    response = client.get("/expenses")
    assert response.status_code == 200

    with app.app_context():
        exists = db.session.get(Expense, expense_id)
        assert exists is not None

# test to check if you delete a non-existing id its an error
def test_delete_error(client):
    # Try to delete an expense that doesnt exist
    response = client.post("/expenses/9999999/delete", follow_redirects=True)

    # make sure you get an error
    assert response.status_code == 404 or b"Error" in response.data

def test_confirm_delete_invalid_expense(client):
    response = client.get("/expenses/999999/deleteconfirm")
    assert response.status_code == 200
    assert b"No expense matching the ID" in response.data
