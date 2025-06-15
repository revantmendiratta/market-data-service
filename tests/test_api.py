from fastapi.testclient import TestClient
from app.main import app # Import our main FastAPI app instance

# Create a TestClient instance based on our app
client = TestClient(app)

def test_read_root():
    """
    Tests the root GET / endpoint.
    """
    # Act: Make a request to the endpoint
    response = client.get("/")

    # Assert: Check that the status code is 200 OK
    assert response.status_code == 200

    # Assert: Check that the response JSON is what we expect
    assert response.json() == {"status": "ok", "message": "Welcome to the Market Data Service!"}