import pytest
from django.urls import reverse
from to_do_app.models.enums.role import Role
from to_do_app.tests.factories import UserFactory
from rest_framework import status
from django.utils import timezone
from datetime import timedelta


@pytest.fixture
def user():
    return UserFactory(
        email="testuser@example.com",
        role=Role.USER.value,
        is_active=True,
        failed_login_attempts=0,
        is_locked=False,
        locked_at=None,
    )


@pytest.mark.django_db
class TestLoginView:
    def test_successful_login(self, api_client, user):
        url = reverse("login")
        login_data = {"email": "testuser@example.com", "password": "Test1234!"}

        response = api_client.post(url, login_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "refresh" in response.data
        assert "access" in response.data

        from rest_framework_simplejwt.tokens import AccessToken

        access_token = AccessToken(response.data["access"])
        assert access_token["email"] == "testuser@example.com"
        assert access_token["role"] == Role.USER.value
        assert user.is_locked is False

    def test_login_with_invalid_password(self, api_client, user):
        url = reverse("login")
        login_data = {"email": "testuser@example.com", "password": "WrongPassword!"}

        response = api_client.post(url, login_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "error" in response.data
        assert "detail" in response.data["error"]
        assert "no active account" in str(response.data["error"]["detail"]).lower()

    def test_login_with_nonexistent_user(self, api_client):
        url = reverse("login")
        login_data = {"email": "nonexistent@example.com", "password": "Test1234!"}

        response = api_client.post(url, login_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "error" in response.data
        assert "detail" in response.data["error"]
        assert "no active account" in str(response.data["error"]["detail"]).lower()

    def test_account_locked_after_multiple_failed_attempts(self, api_client, user):
        url = reverse("login")
        login_data = {"email": "testuser@example.com", "password": "WrongPassword!"}

        for _ in range(3):
            response = api_client.post(url, login_data, format="json")
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user.refresh_from_db()
        assert user.failed_login_attempts == 3
        assert user.is_locked is False

        response = api_client.post(url, login_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "locked" in str(response.data["error"]["detail"]).lower()

        user.refresh_from_db()
        assert user.failed_login_attempts == 4
        assert user.is_locked is True

    def test_login_with_locked_account(self, api_client, user):
        url = reverse("login")
        login_data = {"email": "testuser@example.com", "password": "Test1234!"}

        user.lock_account()
        user.save()

        response = api_client.post(url, login_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "locked" in str(response.data["error"]["detail"]).lower()

    def test_lock_expires_after_24_hours(self, api_client, user):
        url = reverse("login")
        login_data = {"email": "testuser@example.com", "password": "Test1234!"}

        user.lock_account()
        user.locked_at = timezone.now() - timedelta(hours=25)
        user.save()

        response = api_client.post(url, login_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

        user.refresh_from_db()
        assert user.is_locked is False
        assert user.failed_login_attempts == 0
        assert user.locked_at is None

    def test_missing_email_field(self, api_client):
        url = reverse("login")
        login_data = {"password": "Test1234!"}

        response = api_client.post(url, login_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
        assert "email" in response.data["error"]
        assert "required" in str(response.data["error"]["email"]).lower()

    def test_missing_password_field(self, api_client):
        url = reverse("login")
        login_data = {"email": "testuser@example.com"}

        response = api_client.post(url, login_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
        assert "password" in response.data["error"]
        assert "required" in str(response.data["error"]["password"]).lower()

    def test_unauthenticated_access_allowed(self, api_client):
        url = reverse("login")
        login_data = {"email": "testuser@example.com", "password": "Test1234!"}

        UserFactory(email="testuser@example.com", role=Role.USER.value)

        response = api_client.post(url, login_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "refresh" in response.data
        assert "access" in response.data

    def test_rate_limit_exceeded(self, api_client, user):
        url = reverse("login")
        login_data = {"email": "testuser@example.com", "password": "Test1234!"}

        for _ in range(3):
            response = api_client.post(url, login_data, format="json")
            assert response.status_code == status.HTTP_200_OK

        response = api_client.post(url, login_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
