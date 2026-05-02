from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_sqli_vulnerability() -> None:
    """
    Ensure SQL injection allows dumping all users.
    """
    response = client.get(
        "/vulnerable/sqli/search",
        params={"username": "' OR 1=1--"},
    )

    assert response.status_code == 200
    data = response.json()

    # Expect multiple users returned
    assert len(data) >= 2
