from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_sqli_fixed() -> None:
    """
    Ensure SQL injection no longer works.
    """
    response = client.get(
        "/secure/sqli/search",
        params={"username": "' OR 1=1--"},
    )

    assert response.status_code == 200
    data = response.json()

    # Should return no users because exact match required
    assert data == []
