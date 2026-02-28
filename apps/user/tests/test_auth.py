import pytest
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


@pytest.mark.django_db
def test_user_registration(api_client):
    response = api_client.post(
        "/api/users/",
        {
            "username": "newuser",
            "email": "new@example.com",
            "password": "pass1234",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["username"] == "newuser"


@pytest.mark.django_db
def test_login(api_client, create_user):
    create_user(username="john", email="john@test.com", password="pass1234")

    response = api_client.post(
        "/api/login/",
        {"username": "john", "password": "pass1234"},
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_token_refresh(api_client, create_user):
    create_user(username="john", email="john@test.com", password="pass1234")

    login = api_client.post(
        "/api/login/",
        {"username": "john", "password": "pass1234"},
        format="json",
    )

    refresh = login.data["refresh"]

    response = api_client.post(
        "/api/token/refresh/",
        {"refresh": refresh},
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
def test_logout_blacklists_token(api_client, create_user):
    create_user(username="john", email="john@test.com", password="pass1234")

    login = api_client.post(
        "/api/login/",
        {"username": "john", "password": "pass1234"},
        format="json",
    )

    refresh = login.data["refresh"]

    response = api_client.post(
        "/api/logout/",
        {"refresh": refresh},
        format="json",
    )

    assert response.status_code == 200
    assert BlacklistedToken.objects.count() == 1
