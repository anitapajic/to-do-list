import pytest
from rest_framework import serializers
from to_do_app.serializers.auth_serializers.register_serializer import (
    RegisterSerializer,
)
from to_do_app.models import User
from to_do_app.models.enums.role import Role
from to_do_app.tests.factories import UserFactory


@pytest.fixture
def user_data():
    return {
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "12345678!",
        "password2": "12345678!",
        "role": Role.USER.value,
    }


@pytest.mark.django_db
class TestRegisterSerializer:
    def test_valid_data(self, user_data):
        serializer = RegisterSerializer(data=user_data)
        assert serializer.is_valid(raise_exception=True)
        user = serializer.save()

        assert isinstance(user, User)
        assert user.email == "testuser@example.com"
        assert user.name == "Test User"
        assert user.role == Role.USER.value
        assert user.check_password("12345678!")
        assert User.objects.count() == 1

    def test_missing_email(self, user_data):
        user_data.pop("email")
        serializer = RegisterSerializer(data=user_data)

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        errors = exc_info.value.detail
        assert "email" in errors
        assert "required" in str(errors["email"]).lower()

    def test_invalid_email_format(self, user_data):
        user_data["email"] = "invalid-email"
        serializer = RegisterSerializer(data=user_data)

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        errors = exc_info.value.detail
        assert "email" in errors
        assert "valid" in str(errors["email"]).lower()

    def test_duplicate_email(self, user_data):
        UserFactory(email="testuser@example.com")
        serializer = RegisterSerializer(data=user_data)

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        errors = exc_info.value.detail
        assert "email" in errors
        assert "unique" in str(errors["email"]).lower()

    def test_missing_name(self, user_data):
        user_data.pop("name")
        serializer = RegisterSerializer(data=user_data)

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        errors = exc_info.value.detail
        assert "name" in errors
        assert "required" in str(errors["name"]).lower()

    def test_missing_password(self, user_data):
        user_data.pop("password")
        serializer = RegisterSerializer(data=user_data)

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        errors = exc_info.value.detail
        assert "password" in errors
        assert "required" in str(errors["password"]).lower()

    def test_missing_password2(self, user_data):
        user_data.pop("password2")
        serializer = RegisterSerializer(data=user_data)

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        errors = exc_info.value.detail
        assert "password2" in errors
        assert "required" in str(errors["password2"]).lower()

    def test_passwords_dont_match(self, user_data):
        user_data["password2"] = "Different1234!"
        serializer = RegisterSerializer(data=user_data)

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        errors = exc_info.value.detail
        assert "non_field_errors" in errors
        assert "match" in str(errors["non_field_errors"]).lower()

    def test_weak_password(self, user_data):
        user_data["password"] = "123"
        user_data["password2"] = "123"
        serializer = RegisterSerializer(data=user_data)

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        errors = exc_info.value.detail
        assert "password" in errors
        error_messages = str(errors["password"]).lower()
        assert "short" in error_messages

    def test_default_role(self, user_data):
        user_data.pop("role")
        serializer = RegisterSerializer(data=user_data)
        assert serializer.is_valid(raise_exception=True)
        user = serializer.save()

        assert user.role == "USER"
        assert User.objects.count() == 1

    def test_invalid_role(self, user_data):
        user_data["role"] = "INVALID_ROLE"
        serializer = RegisterSerializer(data=user_data)

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        errors = exc_info.value.detail
        assert "role" in errors
        assert (
            "valid" in str(errors["role"]).lower()
            or "choice" in str(errors["role"]).lower()
        )
