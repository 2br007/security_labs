from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_bola_vulnerability() -> None:
    """
    Ensure that a user can access another user's data (BOLA).
    """
    response = client.get(
        "/vulnerable/users/2",
        headers={"X-User-ID": "1"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 2
    assert data["username"] == "bob"
