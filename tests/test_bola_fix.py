from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_bola_fixed_forbidden() -> None:
    """
    Ensure that a user CANNOT access another user's data.
    """
    response = client.get(
        "/secure/users/2",
        headers={"X-User-ID": "1"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to access this resource"


def test_bola_fixed_allowed() -> None:
    """
    Ensure that a user CAN access their own data.
    """
    response = client.get(
        "/secure/users/1",
        headers={"X-User-ID": "1"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["username"] == "alice"
