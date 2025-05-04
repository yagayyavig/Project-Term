# Test the GET /expenses route to ensure it loads correctly
def test_list_expenses(client):
    response = client.get("/expenses")
    assert response.status_code == 200
    # Check for basic page content that confirms the page loaded
    assert b"Expenses" in response.data or b"Add Expense" in response.data