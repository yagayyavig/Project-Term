from db import db
from models.expense import Expense
from models.category import Category
from datetime import datetime, timedelta
from sqlalchemy import select



def create_category(name="Test"):
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return category

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

def test_edit_expense_future_date(client, app):
    with app.app_context():
        category = Category(name="Test FD")
        db.session.add(category)
        db.session.commit()

        category_id = category.id

        expense = Expense(amount=20.0, category=category, date=datetime(2025, 1, 1).date(), note="hello")
        db.session.add(expense)
        db.session.commit()
        expense_id =expense.id

    future_date = (datetime.today() + timedelta(days=10)).strftime("%Y-%m-%d")

    response = client.post(f"/expenses/edit/{expense_id}", data={
        "amount": "50",
        "category_id": str(category_id),
        "date": future_date,
        "note": "Updated expense"
    })

    assert response.status_code == 200
    print(response.data.decode())
    assert b"Cannot set a future date for the expense" in response.data

def test_edit_expense_negative_amount(client, app):
    with app.app_context():
        category = Category(name="Test Category")
        db.session.add(category)
        db.session.commit()
        category_id = category.id

        expense = Expense(
            amount=100.0,
            category_id=category_id,
            date=datetime(2025, 1, 1).date(),
            note="Initial"
        )
        db.session.add(expense)
        db.session.commit()
        expense_id = expense.id

    response = client.post(f"/expenses/edit/{expense_id}", data={
        "amount": "-123.45",
        "category_id": str(category_id),
        "date": "2025-01-02",
        "note": "Trying negative"
    })

    assert response.status_code == 200
    assert b"Cannot add a negative amount!" in response.data

def test_edit_expense_max_amount(client, app):
    with app.app_context():
        category = Category(name="High Roller")
        db.session.add(category)
        db.session.commit()
        category_id = category.id

        expense = Expense(
            amount=100.0,
            category_id=category_id,
            date=datetime(2025, 1, 1).date(),
            note="Initial"
        )
        db.session.add(expense)
        db.session.commit()
        expense_id = expense.id

    response = client.post(f"/expenses/edit/{expense_id}", data={
        "amount": "1000001",  # Just over the max limit
        "category_id": str(category_id),
        "date": "2025-01-02",
        "note": "Trying to go big"
    })

    assert response.status_code == 200
    assert b"Cannot add the amount you suggested" in response.data