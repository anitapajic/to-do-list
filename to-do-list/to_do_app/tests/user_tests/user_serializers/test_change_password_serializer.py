import pytest
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from to_do_app.serializers.user_serializers.change_password_serializer import (
    ChangePasswordSerializer,
)
from to_do_app.models.enums.role import Role
from to_do_app.tests.factories import UserFactory
from unittest.mock import Mock


@pytest.fixture
def request_context(user):
    request = Mock()
    request.user = user
    return {"request": request}


@pytest.mark.django_db
class TestChangePasswordSerializer:
    def test_valid_data(self, user, request_context):
        data = {
            "old_password": "Test1234!",
            "password": "NewPass123!",
            "password2": "NewPass123!",
        }

        serializer = ChangePasswordSerializer(
            instance=user, data=data, context=request_context
        )
        assert serializer.is_valid(raise_exception=True)

        updated_user = serializer.save()
        assert updated_user == user
        updated_user.refresh_from_db()
        assert updated_user.check_password("NewPass123!")
        assert not updated_user.check_password("Test1234!")

    def test_invalid_old_password(self, user, request_context):
        data = {
            "old_password": "WrongPass!",
            "password": "NewPass123!",
            "password2": "NewPass123!",
        }

        serializer = ChangePasswordSerializer(
            instance=user, data=data, context=request_context
        )

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        errors = exc_info.value.detail
        assert "old_password" in errors
        assert "old password is not correct" in str(errors["old_password"]).lower()

        user.refresh_from_db()
        assert user.check_password("Test1234!")

    def test_password_mismatch(self, user, request_context):
        data = {
            "old_password": "Test1234!",
            "password": "NewPass123!",
            "password2": "DifferentPass123!",
        }

        serializer = ChangePasswordSerializer(
            instance=user, data=data, context=request_context
        )

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        errors = exc_info.value.detail
        assert "non_field_errors" in errors
        assert "password fields didn't match" in str(errors["non_field_errors"]).lower()

        user.refresh_from_db()
        assert user.check_password("Test1234!")

    def test_weak_new_password(self, user, request_context):
        data = {"old_password": "Test1234!", "password": "123", "password2": "123"}

        serializer = ChangePasswordSerializer(
            instance=user, data=data, context=request_context
        )

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        errors = exc_info.value.detail
        assert "password" in errors
        assert "short" in str(errors["password"]).lower()

        user.refresh_from_db()
        assert user.check_password("Test1234!")

    def test_missing_required_field(self, user, request_context):
        data = {"old_password": "Test1234!", "password": "NewPass123!"}

        serializer = ChangePasswordSerializer(
            instance=user, data=data, context=request_context
        )

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        errors = exc_info.value.detail
        assert "password2" in errors
        assert "required" in str(errors["password2"]).lower()

    def test_update_different_user(self, user, request_context):
        other_user = UserFactory(
            email="otheruser@example.com", role=Role.USER.value, is_active=True
        )
        data = {
            "old_password": "Test1234!",
            "password": "NewPass123!",
            "password2": "NewPass123!",
        }

        serializer = ChangePasswordSerializer(
            instance=other_user, data=data, context=request_context
        )
        assert serializer.is_valid(raise_exception=True)

        with pytest.raises(PermissionDenied) as exc_info:
            serializer.save()

        assert "permission" in str(exc_info.value).lower()
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

        user.refresh_from_db()
        other_user.refresh_from_db()
        assert user.check_password("Test1234!")
        assert other_user.check_password("Test1234!")
