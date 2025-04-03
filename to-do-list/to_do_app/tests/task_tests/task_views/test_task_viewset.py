import pytest
from django.urls import reverse
from django.utils.timezone import now
from to_do_app.tests.factories import TaskFactory
from to_do_app.models.enums.priority import Priority
from to_do_app.models.enums.task_status import TaskStatus


@pytest.mark.django_db
class TestTaskViewSet:
    def test_task_list_view_authenticated(self, authenticated_client, user):
        task = TaskFactory(owner=user)
        url = reverse("task-list")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == str(task.id)

    def test_task_list_view_unauthenticated(self, api_client):
        url = reverse("task-list")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_task_list_empty(self, authenticated_client):
        url = reverse("task-list")
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_task_create_view_authenticated(self, authenticated_client):
        data = {
            "title": "Test Task",
            "description": "Task Description",
            "due_date": "2025-03-30T11:38:16.454Z",
            "priority": Priority.HIGH.value,
            "status": TaskStatus.PENDING.value,
        }
        url = reverse("task-list")

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == 201
        assert response.data["title"] == "Test Task"

    def test_task_create_invalid_data(self, authenticated_client):
        data = {"title": ""}
        url = reverse("task-list")
        response = authenticated_client.post(url, data, format="json")
        assert response.status_code == 400
        assert "This field may not be blank." in response.data["error"]["title"]

    def test_task_create_view_missing_fields(self, authenticated_client):
        data = {}
        url = reverse("task-list")

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == 400
        assert "This field is required." in response.data["error"]["title"]

    def test_task_update_view_authenticated(self, authenticated_client, user):
        task = TaskFactory(owner=user)
        data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "due_date": "2025-03-30T11:38:16.454Z",
            "priority": Priority.HIGH.value,
            "status": TaskStatus.IN_PROGRESS.value,
        }
        url = reverse("task-detail", kwargs={"pk": task.id})

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == 200
        assert response.data["title"] == "Updated Task"
        assert response.data["status"] == TaskStatus.IN_PROGRESS.value

    def test_task_update_nonexistent(self, authenticated_client):
        url = reverse("task-detail", kwargs={"pk": 999999})
        response = authenticated_client.put(url, {}, format="json")
        assert response.status_code == 404

    def test_task_delete_view_authenticated(self, authenticated_client, user):
        task = TaskFactory(owner=user)
        url = reverse("task-detail", kwargs={"pk": task.id})

        response = authenticated_client.delete(url)

        assert response.status_code == 204

    def test_task_delete_nonexistent(self, authenticated_client):
        url = reverse("task-detail", kwargs={"pk": 9999999})
        response = authenticated_client.delete(url)
        assert response.status_code == 404

    def test_task_filter_view(self, authenticated_client, user):
        task1 = TaskFactory(
            owner=user,
            status=TaskStatus.PENDING.value,
            priority="High",
            due_date="2025-03-30T11:38:16.454Z",
        )
        TaskFactory(
            owner=user,
            status=TaskStatus.COMPLETED.value,
            priority="Low",
            due_date="2025-03-31T11:38:16.454Z",
        )
        url = reverse("task-list")

        response = authenticated_client.get(url + "?status=Pending")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == str(task1.id)

    def test_task_filter_invalid_status(self, authenticated_client):
        url = reverse("task-list")
        response = authenticated_client.get(url + "?status=InvalidStatus")
        assert response.status_code == 400

    def test_task_search_view(self, authenticated_client, user):
        task1 = TaskFactory(
            owner=user, title="Test Task 1", description="Description 1"
        )
        TaskFactory(
            owner=user, title="Another Task", description="Description 2"
        )
        url = reverse("task-list")

        response = authenticated_client.get(url + "?search=Test Task 1")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == str(task1.id)

    def test_task_search_no_results(self, authenticated_client):
        url = reverse("task-list")

        response = authenticated_client.get(url + "?search=NonExistent")
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_task_invalid_id(self, authenticated_client):
        invalid_task_id = 999999

        url = reverse("task-detail", kwargs={"pk": invalid_task_id})

        response = authenticated_client.get(url)

        assert response.status_code == 404

    def test_subtasks(self, authenticated_client, user):
        parent = TaskFactory(owner=user)
        TaskFactory(owner=user, parent=parent)
        url = reverse("task-subtasks", args=[parent.id])

        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 1

    def test_sorted_by_priority(self, authenticated_client, user):
        TaskFactory(owner=user, priority=Priority.HIGH.value)
        TaskFactory(owner=user, priority=Priority.LOW.value)
        url = reverse("task-sorted-by-priority")

        response = authenticated_client.get(url)

        assert response.status_code == 200

    def test_get_overdue(self, authenticated_client, user):
        TaskFactory(owner=user, due_date=now().date().replace(day=1))
        url = reverse("task-get-overdue")

        response = authenticated_client.get(url)

        assert response.status_code == 200

    def test_get_due_today(self, authenticated_client, user):
        TaskFactory(owner=user, due_date=now().date())
        url = reverse("task-get-due-today")

        response = authenticated_client.get(url)

        assert response.status_code == 200

    def test_bulk_delete(self, authenticated_client, user):
        tasks = TaskFactory.create_batch(3, owner=user)
        url = reverse("task-bulk-delete")

        response = authenticated_client.delete(url, {"ids": [task.id for task in tasks]}, format="json")

        assert response.status_code == 204

    def test_bulk_delete_invalid_ids(self, authenticated_client):
        url = reverse("task-bulk-delete")

        response = authenticated_client.delete(url, {"ids": [999999, 888888]}, format="json")

        assert response.status_code == 404

    def test_bulk_update(self, authenticated_client, user):
        tasks = TaskFactory.create_batch(3, owner=user)
        url =  reverse("task-bulk-update")

        response = authenticated_client.patch(
            url, 
            {"ids": [str(task.id) for task in tasks], "data": {"priority": Priority.HIGH.value}}, 
            format="json")

        assert response.status_code == 200

    def test_bulk_update_invalid_data(self, authenticated_client):
        url =  reverse("task-bulk-update")

        response = authenticated_client.patch(
            url, 
            {"ids": [], "data": {}}, 
            format="json")

        assert response.status_code == 400