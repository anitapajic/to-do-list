import pytest
from rest_framework.exceptions import ValidationError
from to_do_app.serializers.user_serializers.user_serializer import UserSerializer
from to_do_app.tests.factories import UserFactory


@pytest.mark.django_db
class TestUpdateUserSerializer:
    def test_valid_data(self, user):
        data = {
            "email": "newemail@example.com",
            "name": "Updated Name",
        }

        serializer = UserSerializer(instance=user, data=data)

        assert serializer.is_valid()

        updated_user = serializer.save()
        assert updated_user.email == data["email"]
        assert updated_user.name == data["name"]

    def test_email_already_exists(self):
        user1 = UserFactory(email="user1@example.com")
        user2 = UserFactory(email="user2@example.com")

        data = {
            "email": user1.email,
            "name": "Updated Name",
        }

        serializer = UserSerializer(instance=user2, data=data)

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_no_changes(self, user):
        data = {
            "email": user.email,
            "name": user.name,
        }

        serializer = UserSerializer(instance=user, data=data)

        assert serializer.is_valid()

        updated_user = serializer.save()
        assert updated_user == user

    def test_partial_update(self, user):
        data = {
            "name": "New Name",
        }

        serializer = UserSerializer(instance=user, data=data, partial=True)

        assert serializer.is_valid()

        updated_user = serializer.save()
        assert updated_user.name == data["name"]
        assert updated_user.email == user.email

    def test_invalid_email_format(self, user):
        data = {
            "email": "invalid-email",
            "name": "Updated Name",
        }

        serializer = UserSerializer(instance=user, data=data)
        assert not serializer.is_valid()

        assert "email" in serializer.errors
