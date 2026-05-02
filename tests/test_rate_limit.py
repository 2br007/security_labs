from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_no_rate_limit() -> None:
    """
    Ensure repeated login attempts are allowed.
    """
    responses = []

    for _ in range(10):
        r = client.post(
            "/vulnerable/auth/login",
            params={"username": "alice"},
        )
        responses.append(r.status_code)

    # All requests succeed → no rate limit
    assert all(status == 200 for status in responses)
