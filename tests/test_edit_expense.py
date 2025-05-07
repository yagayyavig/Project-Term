from db import db
from models.expense import Expense
from datetime import datetime

def test_edit_expense_get(client, app):
    # Test the GET method for editing an expense
    with app.app_context():
        # Add test expense
        expense = Expense(
            amount=10.0,
            category="Groceries",
            date=datetime(2025, 1, 1).date(),
            note="milk"
        )
    db.session.add(expense)
    db.session.commit()
    expense_id = expense.id

    # Sends a GET request to edit page using client
    response = client.get(f"/expenses/edit/{expense_id}")

    # Checks that the page is loading and the data is present
    assert response.status_code == 200
    assert b"Edit Expense" in response.data
    assert b"Groceries" in response.data
    assert b"milk" in response.data