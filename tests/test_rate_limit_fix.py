from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_rate_limit_blocks_requests() -> None:
    """
    Ensure rate limiting blocks excessive requests.
    """

    # exceed limit (3 requests)
    for _ in range(3):
        client.post(
            "/secure/auth/login",
            params={"username": "alice"},
        )

    response = client.post(
        "/secure/auth/login",
        params={"username": "alice"},
    )

    assert response.status_code == 429
    assert response.json()["detail"] == "Too many requests"
