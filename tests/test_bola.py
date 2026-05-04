def test_bola_vulnerability(client, create_user):
    """
    Ensure that a user can access another user's data (BOLA).
    """

    user1 = create_user("alice")
    user2 = create_user("bob")

    response = client.get(
        f"/vulnerable/users/{user2.id}",
        headers={"X-User-ID": str(user1.id)},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == user2.id
    assert data["username"] == "bob"
