import pytest
from django.urls import reverse
from rest_framework import status
from to_do_app.models import User
from to_do_app.models.enums.role import Role
from to_do_app.tests.factories import UserFactory


@pytest.fixture
def register_data():
    return {
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "Test1234!",
        "password2": "Test1234!",
        "role": Role.USER.value,
    }


@pytest.mark.django_db
class TestRegisterView:
    def test_successful_registration(self, api_client, register_data):
        url = reverse("register")

        response = api_client.post(url, register_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "User registered successfully!"
        assert "user" in response.data
        assert response.data["user"]["email"] == "testuser@example.com"
        assert response.data["user"]["name"] == "Test User"
        assert response.data["user"]["role"] == Role.USER.value
        assert User.objects.count() == 1

    def test_duplicate_email_registration(self, api_client, register_data):
        existing_user = UserFactory(email="testuser@example.com")
        url = reverse("register")

        response = api_client.post(url, register_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_dict = response.data["error"]
        assert "email" in error_dict
        assert "unique" in str(error_dict["email"]).lower()
        assert User.objects.count() == 1
        assert User.objects.first().id == existing_user.id

    def test_missing_required_fields(self, api_client, register_data):
        url = reverse("register")
        register_data.pop("email")

        response = api_client.post(url, register_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_dict = response.data["error"]
        assert "email" in error_dict
        assert "required" in str(error_dict["email"]).lower()
        assert User.objects.count() == 0

    def test_invalid_email_format(self, api_client, register_data):
        url = reverse("register")
        register_data["email"] = "invalid-email"

        response = api_client.post(url, register_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_dict = response.data["error"]
        assert "email" in error_dict
        assert "valid" in str(error_dict["email"]).lower()
        assert User.objects.count() == 0

    def test_weak_password(self, api_client, register_data):
        url = reverse("register")
        register_data["password"] = "123"
        register_data["password2"] = "123"

        response = api_client.post(url, register_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_dict = response.data["error"]
        assert "password" in error_dict
        error_messages = str(error_dict["password"]).lower()
        assert "short" in error_messages
        assert "common" in error_messages
        assert "numeric" in error_messages
        assert User.objects.count() == 0

    def test_invalid_role(self, api_client, register_data):
        url = reverse("register")
        register_data["role"] = ("INVALID_ROLE",)

        response = api_client.post(url, register_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_dict = response.data["error"]
        assert "role" in error_dict
        assert "choice" in str(error_dict["role"]).lower()
        assert User.objects.count() == 0

    def test_unauthenticated_access(self, api_client, register_data):
        url = reverse("register")

        response = api_client.post(url, register_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        created_user = User.objects.first()
        assert created_user.email == "testuser@example.com"
        assert created_user.name == "Test User"
        assert created_user.role == Role.USER.value
