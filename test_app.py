from datetime import datetime, timedelta
from app import app as flask_app
from db import db
from models.expense import Expense
import pytest

# Set up the Flask application for testing with an in-memory SQLite database
@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with flask_app.app_context():
        db.create_all()  # Create all database tables
        yield flask_app
        db.drop_all()    # Clean up after each test run

# Create a test client for making HTTP requests to the Flask app
@pytest.fixture
def client(app):
    return app.test_client()

# Test the GET /expenses route to ensure it loads correctly
def test_list_expenses(client):
    response = client.get("/expenses")
    assert response.status_code == 200
    # Check for basic page content that confirms the page loaded
    assert b"Expenses" in response.data or b"Add Expense" in response.data

# Test the GET /expenses/add route to ensure the Add Expense form loads
def test_add_expense_get(client):
    response = client.get("/expenses/add")
    assert response.status_code == 200
    # Check that the form fields or heading are present
    assert b"Add Expense" in response.data or b"amount" in response.data

# Test POST /expenses/add with a future date, which should fail with an error
def test_add_expense_future_date(client):
    future_date = (datetime.today() + timedelta(days=5)).strftime("%Y-%m-%d")
    response = client.post("/expenses/add", data={
        "amount": "100",
        "category": "Travel",
        "date": future_date,
        "note": "Testing future"
    })
    assert response.status_code == 200
    # Check that the specific error message appears in the response
    assert b"Cannot add expense for a future date!" in response.data

# Test POST /expenses/add with valid data and follow redirect to /expenses
def test_add_expense_valid(client):
    today = datetime.today().strftime("%Y-%m-%d")
    response = client.post("/expenses/add", data={
        "amount": "75.5",
        "category": "Food",
        "date": today,
        "note": "Test lunch"
    }, follow_redirects=True)
    assert response.status_code == 200
    # Ensure the newly added expense is rendered on the page
    assert b"Food" in response.data or b"Test lunch" in response.data
