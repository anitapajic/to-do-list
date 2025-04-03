import pytest
from django.urls import reverse
from rest_framework import status
from to_do_app.tests.factories import UserFactory
from to_do_app.models.enums.role import Role


@pytest.mark.django_db
class TestChangePasswordView:
    def test_successful_password_change(self, authenticated_client, user):
        url = reverse("change-password", kwargs={"pk": user.pk})
        data = {
            "old_password": "Test1234!",
            "password": "NewPass123!",
            "password2": "NewPass123!",
        }

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK, (
            f"Failed with: {response.data}"
        )

        user.refresh_from_db()
        assert user.check_password("NewPass123!")
        assert not user.check_password("Test1234!")

    def test_invalid_old_password(self, authenticated_client, user):
        url = reverse("change-password", kwargs={"pk": user.pk})
        data = {
            "old_password": "WrongPass!",
            "password": "NewPass123!",
            "password2": "NewPass123!",
        }

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
        assert "old_password" in response.data["error"]
        assert "not correct" in str(response.data["error"]["old_password"]).lower()

        user.refresh_from_db()
        assert user.check_password("Test1234!")

    def test_password_mismatch(self, authenticated_client, user):
        url = reverse("change-password", kwargs={"pk": user.pk})
        data = {
            "old_password": "Test1234!",
            "password": "NewPass123!",
            "password2": "DifferentPass123!",
        }

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
        assert (
            "password2" in response.data["error"]
            or "non_field_errors" in response.data["error"]
        )
        assert "match" in str(response.data["error"]).lower()

        user.refresh_from_db()
        assert user.check_password("Test1234!")

    def test_unauthenticated_access(self, api_client, user):
        url = reverse("change-password", kwargs={"pk": user.pk})
        data = {
            "old_password": "Test1234!",
            "password": "NewPass123!",
            "password2": "NewPass123!",
        }

        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.data["error"]
        assert (
            "authentication credentials"
            in str(response.data["error"]["detail"]).lower()
        )

        user.refresh_from_db()
        assert user.check_password("Test1234!")

    def test_change_another_user_password(self, authenticated_client, user):
        other_user = UserFactory(
            email="otheruser@example.com", role=Role.USER.value, is_active=True
        )
        url = reverse("change-password", kwargs={"pk": other_user.pk})
        data = {
            "old_password": "Test1234!",
            "password": "NewPass123!",
            "password2": "NewPass123!",
        }

        response = authenticated_client.put(url, data, format="json")

        assert (
            response.status_code == status.HTTP_403_FORBIDDEN
            or response.status_code == status.HTTP_404_NOT_FOUND
        )
        assert "error" in response.data

        user.refresh_from_db()
        assert user.check_password("Test1234!")

        other_user.refresh_from_db()
        assert other_user.check_password("Test1234!")
