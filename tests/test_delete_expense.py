from db import db
from models.expense import Expense
from datetime import datetime

#test the confirm delete actally deltetes
def test_confirm_delete_button(client, app):
    #Create mock expense for testing 
    with app.app_context():
        expense = Expense(
            amount=10.0,
            category="Dont matter",
            note="Test",
            date=datetime(2025, 1, 1)
        )
        db.session.add(expense)
        db.session.commit()
        expense_id = expense.id

    # make sure the page loads with confirm button 
    response = client.get(f"/expenses/{expense_id}/deleteconfirm")
    assert response.status_code == 200
    assert b"Confirm Deletion" in response.data

    # "press" confirm delete 
    response = client.post(f"/expenses/{expense_id}/delete", follow_redirects=True)
    assert response.status_code == 200

    # Check expense is deleted (not in db)
    with app.app_context():
        deleted = db.session.get(Expense, expense_id)
        assert deleted is None


# test the cancel does nothing 
def test_cancel_button(client, app):
    #Create mock expense for testing 
    with app.app_context():
        expense = Expense(
            amount=10.0,
            category="Dont matter",
            note="Test",
            date=datetime(2025, 1, 1)
        )
        db.session.add(expense)
        db.session.commit()
        expense_id = expense.id

    # make sure the page loads with the cancel button
    response = client.get(f"/expenses/{expense_id}/deleteconfirm")
    assert response.status_code == 200
    assert b"Cancel" in response.data

    # "press" cancel (do nothing)
    response = client.get("/expenses")
    assert response.status_code == 200

    # Check expense is NOT deleted (is in db)
    with app.app_context():
        exists = db.session.get(Expense, expense_id)
        assert exists is not None
