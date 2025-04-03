import pytest
from django.urls import reverse
from rest_framework import status
from to_do_app.models.enums.role import Role
from to_do_app.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserViewSet:
    @pytest.fixture
    def admin_user(self):
        return UserFactory(role=Role.ADMIN.value)

    @pytest.fixture
    def normal_user(self):
        return UserFactory(role=Role.USER.value)


    def test_create_user_as_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("user-list")

        data = {
            "email": "newuser@example.com",
            "name": "New User",
            "role": Role.USER.value,
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == data["email"]
        assert response.data["name"] == data["name"]

    def test_create_user_as_normal_user(self, api_client, normal_user):
        api_client.force_authenticate(user=normal_user)
        url = reverse("user-list")
        data = {
            "email": "newuser@example.com",
            "name": "New User",
            "role": Role.USER.value,
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["error"]["detail"]
            == "You do not have permission to perform this action."
        )

    def test_update_user_as_admin(self, api_client, admin_user):
        user = UserFactory()
        api_client.force_authenticate(user=admin_user)
        url = reverse("user-detail", kwargs={"pk": user.id})

        data = {"email": "updateduser@example.com", "name": "Updated Name"}

        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == data["email"]
        assert response.data["name"] == data["name"]

    def test_update_user_as_owner(self, api_client, normal_user):
        user = normal_user
        api_client.force_authenticate(user=normal_user)
        url = reverse("user-detail", kwargs={"pk": user.id})

        data = {"email": "updateduser@example.com", "name": "Updated Name"}

        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == data["email"]
        assert response.data["name"] == data["name"]

    def test_update_user_as_non_owner(self, api_client, normal_user):
        user = UserFactory()
        api_client.force_authenticate(user=normal_user)
        url = reverse("user-detail", kwargs={"pk": user.id})

        data = {"email": "updateduser@example.com", "name": "Updated Name"}

        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["error"]["authorize"] == "You don't have permission to edit this user."

    def test_destroy_user_as_admin(self, api_client, admin_user):
        user = UserFactory()
        api_client.force_authenticate(user=admin_user)
        url = reverse("user-detail", kwargs={"pk": user.id})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["message"] == "User deleted successfully."

    def test_destroy_user_as_normal_user(self, api_client, normal_user):
        user = UserFactory()
        api_client.force_authenticate(user=normal_user)
        url = reverse("user-detail", kwargs={"pk": user.id})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["error"]["detail"] == "You do not have permission to perform this action."

    def test_retrieve_user_as_admin_user(self, api_client, admin_user):
        user = UserFactory()
        api_client.force_authenticate(user=admin_user)
        url = reverse("user-detail", kwargs={"pk": user.id})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(user.id)
        assert response.data["email"] == user.email
        assert response.data["name"] == user.name

    def test_retrieve_user_as_unauthenticated_user(self, api_client):
        user = UserFactory()
        url = reverse("user-detail", kwargs={"pk": user.id})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.data["error"]["detail"] == "Authentication credentials were not provided."
        )

    def test_list_users_as_admin(self, api_client, admin_user):
        UserFactory()
        UserFactory()
        api_client.force_authenticate(user=admin_user)
        url = reverse("user-list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 2

    def test_list_users_as_normal_user(self, api_client, normal_user):
        UserFactory()
        UserFactory()
        api_client.force_authenticate(user=normal_user)
        url = reverse("user-list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["error"]["detail"]
            == "You do not have permission to perform this action."
        )
