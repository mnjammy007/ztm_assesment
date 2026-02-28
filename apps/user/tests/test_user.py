import pytest


@pytest.mark.django_db
def test_user_retrieve_self(authenticated_client):
    client, user = authenticated_client

    response = client.get(f"/api/users/{user.id}/")

    assert response.status_code == 200
    assert response.data["username"] == user.username


@pytest.mark.django_db
def test_cross_user_access_blocked(api_client, create_user):
    user1 = create_user("user1", "u1@test.com", "pass1234")
    user2 = create_user("user2", "u2@test.com", "pass1234")

    login = api_client.post(
        "/api/login/",
        {"username": "user1", "password": "pass1234"},
        format="json",
    )

    access = login.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    response = api_client.get(f"/api/users/{user2.id}/")

    assert response.status_code in (403, 404)


@pytest.mark.django_db
def test_password_change_invalidates_refresh(api_client, create_user):
    user = create_user("john", "john@test.com", "pass1234")

    login = api_client.post(
        "/api/login/",
        {"username": "john", "password": "pass1234"},
        format="json",
    )

    refresh = login.data["refresh"]
    access = login.data["access"]

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    # Change password
    response = api_client.put(
        f"/api/users/{user.id}/",
        {
            "username": "john",
            "email": "john@test.com",
            "password": "newpass123",
        },
        format="json",
    )

    assert response.status_code == 200

    # Old refresh should now fail
    refresh_response = api_client.post(
        "/api/token/refresh/",
        {"refresh": refresh},
        format="json",
    )

    assert refresh_response.status_code == 401
