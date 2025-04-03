import pytest
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from to_do_app.models.enums.task_status import TaskStatus
from to_do_app.tests.factories import TaskFactory


@pytest.mark.django_db
class TestReportView:
    def test_unauthenticated_access(self, api_client):
        response = api_client.get("/api/reports/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_valid_report_data(self, authenticated_client, user):
        base_time = timezone.now() - timedelta(days=3)
        created_time = base_time
        completed_time = created_time + timedelta(days=1)

        TaskFactory.create_batch(
            3,
            owner=user,
            status=TaskStatus.COMPLETED.value,
            created=created_time,
            completed_at=completed_time,
        )

        response = authenticated_client.get("/api/reports/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["total_tasks"] == 3
        assert data["completed_tasks"] == 3
        assert data["overdue_percentage"] == 0
        avg_hours = data["avg_completion_time_hours"]
        assert 23.0 <= avg_hours <= 25.0

    def test_empty_task_list(self, authenticated_client, user):
        response = authenticated_client.get("/api/reports/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data == {
            "total_tasks": 0,
            "completed_tasks": 0,
            "overdue_percentage": 0.0,
            "avg_completion_time_hours": 0.0,
        }

    def test_partial_completion_data(self, authenticated_client, user):
        base_time = timezone.now() - timedelta(days=3)
        created_time = base_time
        completed_time = created_time + timedelta(days=1)

        TaskFactory(
            owner=user,
            status=TaskStatus.COMPLETED.value,
            created=created_time,
            completed_at=completed_time,
        )
        TaskFactory(
            owner=user,
            status=TaskStatus.COMPLETED.value,
            created=base_time + timedelta(days=1),
            completed_at=None,
        )

        response = authenticated_client.get("/api/reports/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["total_tasks"] == 2
        assert data["completed_tasks"] == 2
        avg_hours = data["avg_completion_time_hours"]
        assert 24.0 <= avg_hours <= 48.0

    def test_method_not_allowed(self, authenticated_client):
        response = authenticated_client.post("/api/reports/", {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = authenticated_client.put("/api/reports/", {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_rate_limit(self, authenticated_client):
        for _ in range(97):
            response = authenticated_client.get("/api/reports/")
            assert response.status_code == status.HTTP_200_OK

        response = authenticated_client.get("/api/reports/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
