import pytest
from apps.task.models import Task
from apps.task.views import TaskViewSet


@pytest.mark.django_db
def test_create_task(authenticated_client):
    client, _ = authenticated_client

    response = client.post(
        "/api/tasks/",
        {"title": "Task 1", "description": "Test", "completed": False},
        format="json",
    )

    assert response.status_code == 201
    assert response.data["title"] == "Task 1"


@pytest.mark.django_db
def test_list_tasks(authenticated_client):
    client, _ = authenticated_client

    client.post(
        "/api/tasks/",
        {"title": "Task 1", "description": "Test", "completed": False},
        format="json",
    )

    response = client.get("/api/tasks/")

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_cross_user_task_access_blocked(api_client, create_user):
    user1 = create_user("user1", "u1@test.com", "pass1234")
    user2 = create_user("user2", "u2@test.com", "pass1234")

    # user1 creates task
    login1 = api_client.post(
        "/api/login/",
        {"username": "user1", "password": "pass1234"},
        format="json",
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {login1.data['access']}")

    create_task = api_client.post(
        "/api/tasks/",
        {"title": "Private Task", "description": "Secret", "completed": False},
        format="json",
    )

    task_id = create_task.data["id"]

    # login as user2
    login2 = api_client.post(
        "/api/login/",
        {"username": "user2", "password": "pass1234"},
        format="json",
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {login2.data['access']}")

    response = api_client.get(f"/api/tasks/{task_id}/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_task_str_representation(create_user):
    user = create_user()
    task = Task.objects.create(
        user=user,
        title="Test Task",
        description="Desc",
    )
    assert str(task) == "Test Task"


@pytest.mark.django_db
def test_filter_tasks_by_completed(authenticated_client):
    client, _ = authenticated_client

    client.post(
        "/api/tasks/",
        {
            "title": "Done Task",
            "description": "Done",
            "completed": True,
        },
        format="json",
    )

    client.post(
        "/api/tasks/",
        {
            "title": "Pending Task",
            "description": "Pending",
            "completed": False,
        },
        format="json",
    )

    response = client.get("/api/tasks/?completed=true")

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["completed"] is True


def test_swagger_fake_view_queryset(create_user):
    view = TaskViewSet()
    view.swagger_fake_view = True

    queryset = view.get_queryset()

    assert queryset.count() == 0
