import pytest
from apps.user.models import User


@pytest.mark.django_db
def test_user_str_representation(create_user):
    user = create_user(username="john", email="john@test.com", password="pass1234")
    assert str(user) == "john"


@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(
        username="admin",
        email="admin@test.com",
        password="adminpass123",
    )

    assert user.is_staff is True
    assert user.is_superuser is True


@pytest.mark.django_db
def test_create_user_validation():
    with pytest.raises(ValueError):
        User.objects.create_user(username="", password="pass1234")

    with pytest.raises(ValueError):
        User.objects.create_user(username="user", password=None)


@pytest.mark.django_db
def test_get_by_natural_key(create_user):
    create_user(username="john", email="john@test.com", password="pass1234")

    user = User.objects.get_by_natural_key("john")
    assert user.username == "john"
