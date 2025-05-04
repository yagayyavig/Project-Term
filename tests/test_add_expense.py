from datetime import datetime, timedelta


def test_add_expense_get(client):
    response = client.get("/expenses/add")
    assert response.status_code == 200
    assert b"Add Expense" in response.data or b"amount" in response.data

def test_add_expense_future_date(client):
    future_date = (datetime.today() + timedelta(days=5)).strftime("%Y-%m-%d")
    response = client.post("/expenses/add", data={
        "amount": "100",
        "category": "Travel",
        "date": future_date,
        "note": "Testing future"
    })
    assert response.status_code == 200
    assert b"Cannot add expense for a future date!" in response.data

def test_add_expense_valid(client):
    today = datetime.today().strftime("%Y-%m-%d")
    response = client.post("/expenses/add", data={
        "amount": "75.5",
        "category": "Food",
        "date": today,
        "note": "Test lunch"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Food" in response.data or b"Test lunch" in response.data
