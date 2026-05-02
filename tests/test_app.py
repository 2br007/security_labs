from fastapi.testclient import TestClient

from app.main import app

client: TestClient = TestClient(app)


def test_root() -> None:
    """
    Test the root endpoint returns a 200 OK
    and the expected response payload.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Security Lab is running"}
