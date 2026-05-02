from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_path_traversal_blocked() -> None:
    """
    Ensure traversal attempts are blocked.
    """
    response = client.get(
        "/secure/path/read",
        params={"filename": "../../../../../../../etc/passwd"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Access denied"


def test_path_traversal_allowed() -> None:
    """
    Ensure valid file access still works.
    """
    response = client.get(
        "/secure/path/read",
        params={"filename": "helloworld.txt"},
    )

    assert response.status_code == 200
    assert "Hello" in response.json()["content"]
