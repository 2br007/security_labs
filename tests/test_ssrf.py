from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ssrf_vulnerability() -> None:
    """
    Ensure internal service can be accessed via SSRF.
    """
    response = client.get(
        "/vulnerable/ssrf/fetch",
        params={"url": "http://localhost:8000/internal/metadata"},
    )

    assert response.status_code == 200
    data = response.json()

    assert "SUPER_SECRET_KEY" in data["content"]
