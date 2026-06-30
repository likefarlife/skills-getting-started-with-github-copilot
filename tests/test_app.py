from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_them_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_participant_fails_when_not_signed_up():
    activity_name = "Basketball Team"
    email = "student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()
