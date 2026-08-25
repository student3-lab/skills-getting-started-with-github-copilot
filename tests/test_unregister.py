from urllib.parse import quote


def test_unregister_success_removes_participant(client):
    activity_name = "Basketball Team"
    email = "ava@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants/{quote(email, safe='')}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        f"/activities/{quote('Unknown Club', safe='')}/participants/{quote('test@mergington.edu', safe='')}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    activity_name = "Drama Club"
    missing_email = "not-registered@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants/{quote(missing_email, safe='')}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up"
