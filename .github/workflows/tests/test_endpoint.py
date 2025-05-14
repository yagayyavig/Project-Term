from src.main import app

def test_endpoint():
    client = app.test_client()
    response = client.get('/')
    data = response.json
    assert data['course'] == 'ACIT1515'