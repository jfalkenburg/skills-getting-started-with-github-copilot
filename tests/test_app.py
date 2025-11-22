import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "signupstudent@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    assert "already signed up" in response_dup.json()["detail"]


def test_unregister_from_activity():
    email = "unregstudent@mergington.edu"
    activity = "Chess Club"
    # Ensure not already registered
    # Remove participant if present, ignore errors
    client.post(f"/activities/{activity}/unregister?email={email}")
    # Register first
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    print("Signup response:", signup_response.status_code, signup_response.text)
    assert signup_response.status_code == 200
    # Now unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    print("Unregister response:", response.status_code, response.text)
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    # Unregister again should fail
    response_dup = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_dup.status_code == 400
    assert "not registered" in response_dup.json()["detail"]
