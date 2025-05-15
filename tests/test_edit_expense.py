from db import db
from models.expense import Expense
from models.category import Category
from datetime import datetime
from sqlalchemy import select

# Test the GET method for editing an expense
def test_edit_expense_get(client, app):
    with app.app_context():
        # Add test category
        category = Category(name="Groceries 🛒")
        db.session.add(category)
        db.session.commit()
        # Add test expense
        expense = Expense(
            amount=10.0,
            category=category,
            date=datetime(2025, 1, 1).date(),
            note="milk"
        )
    db.session.add(expense)
    db.session.commit()
    expense_id = expense.id # Save the id to use it in the request

    # Sends a GET request to edit page using client
    response = client.get(f"/expenses/edit/{expense_id}")

    # Checks that the page is loading (status code 200) and the original data is present
    assert response.status_code == 200
    assert b"Edit Expense" in response.data # response.data is type: bytes
    assert b"Groceries" in response.data # b is added to b"All Expenses" str to match data type 
    assert b"milk" in response.data # & compare bytes objects properly
    # An alternative to not add "b" to str is to decode the response:
    # html = response.data.decode()

# Test the POST method for editing an expense
def test_edit_expense_post(client, app):
    with app.app_context():
        # Add category and updated category
        category = Category(name="Groceries 🛒")
        updated_category = Category(name="Dining Out 🍽️")
        db.session.add_all([category, updated_category])
        db.session.commit()
        # Add test expense to edit
        expense = Expense(
            amount=10.0,
            category=category,
            date=datetime(2025, 1, 1).date(),
            note="milk"
        )
        db.session.add(expense)
        db.session.commit()
        expense_id = expense.id
        new_category_id = updated_category.id

    # Sent POST request with updated data to the same URL
    response = client.post(f"/expenses/edit/{expense_id}", data={
        "amount": "20.50",
        "category_id": str(new_category_id),
        "date": "2025-01-05",
        "note": "updated note"
    }, follow_redirects=True) # follow_redirects=True allows to check the final page

    # The request should redirect to the expenses list
    assert response.status_code == 200
    assert b"The Ledger" in response.data # Basic confirmation page loaded

    # Confirms that the database was actually updated
    with app.app_context():
        stmt = select(Expense).where(Expense.id == expense_id)
        updated = db.session.execute(stmt).scalars().first()
        assert updated.amount == 20.50
        assert updated.category.name == "Dining Out 🍽️"
        assert updated.date == datetime(2025, 1, 5).date()
        assert updated.note == "updated note"