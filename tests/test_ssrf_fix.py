from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ssrf_blocked() -> None:
    """
    Ensure internal SSRF is blocked.
    """
    response = client.get(
        "/secure/ssrf/fetch",
        params={"url": "http://localhost:8000/internal/metadata"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "URL not allowed"
