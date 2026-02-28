import pytest
from rest_framework.test import APIClient
from apps.user.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(username="user", email="user@example.com", password="pass1234"):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

    return _create_user


@pytest.fixture
def authenticated_client(api_client, create_user):
    user = create_user()
    response = api_client.post(
        "/api/login/",
        {"username": "user", "password": "pass1234"},
        format="json",
    )
    access = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return api_client, user
