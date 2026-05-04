def test_bola_fixed_allowed(client, create_user, auth_headers):
    user = create_user("alice")

    headers = auth_headers(user.id)

    response = client.get(
        f"/secure/users/{user.id}",
        headers=headers,
    )

    assert response.status_code == 200


def test_bola_fixed_forbidden(client, create_user, auth_headers):
    """
    User cannot access other users' resources.
    """
    user1 = create_user("alice")
    user2 = create_user("bob")

    headers = auth_headers(user1.id)

    response = client.get(
        f"/secure/users/{user2.id}",
        headers=headers,
    )

    assert response.status_code == 403


def test_bola_fixed_not_exist(client, create_user):
    """
    User cannot access without token
    """

    create_user("alice")
    create_user("bob")

    response = client.get(
        "/secure/users/3",
    )

    assert response.status_code == 401


def test_ssrf_blocked(client):
    response = client.get(
        "/secure/ssrf/fetch",
        params={"url": "http://localhost:8000/internal/metadata"},
    )

    assert response.status_code == 400
