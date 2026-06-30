from copy import deepcopy
from urllib.parse import quote
from uuid import uuid4

from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def test_get_activities_returns_seeded_data():
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["max_participants"] == 12


def test_signup_for_activity_adds_participant():
    activity_name = "Basketball Team"
    email = f"{uuid4().hex}@mergington.edu"

    response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_rejects_duplicate_registration():
    activity_name = "Chess Club"
    email = f"{uuid4().hex}@mergington.edu"

    first_response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()
