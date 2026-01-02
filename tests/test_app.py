import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Club" in data
    assert "participants" in data["Basketball Club"]

def test_signup_success():
    # Sign up a new student
    response = client.post("/activities/Basketball%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]

    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "test@mergington.edu" in data["Basketball Club"]["participants"]

def test_signup_duplicate():
    # Try to sign up again
    response = client.post("/activities/Basketball%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=test2@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # First sign up
    client.post("/activities/Soccer%20Team/signup?email=test3@mergington.edu")
    # Then unregister
    response = client.delete("/activities/Soccer%20Team/unregister?email=test3@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]

    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "test3@mergington.edu" not in data["Soccer Team"]["participants"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Art%20Club/unregister?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]

def test_unregister_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert "Mergington High School" in response.text