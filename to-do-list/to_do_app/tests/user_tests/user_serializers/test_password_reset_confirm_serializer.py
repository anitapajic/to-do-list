import pytest
from to_do_app.serializers.user_serializers.password_reset_confirm_serializer import (
    PasswordResetConfirmSerializer,
)


@pytest.mark.django_db
class TestPasswordResetConfirmSerializer:
    def test_valid_password_reset(self, user):
        data = {"new_password": "NewPassword123!"}

        serializer = PasswordResetConfirmSerializer(data=data)

        assert serializer.is_valid()

        user = serializer.save(user)

        assert user.check_password("NewPassword123!") is True

    def test_invalid_password_reset(self, user):
        data = {"new_password": "short"}

        serializer = PasswordResetConfirmSerializer(data=data)

        assert not serializer.is_valid()

        assert "new_password" in serializer.errors

    def test_missing_password_reset(self, user):
        data = {}

        serializer = PasswordResetConfirmSerializer(data=data)

        assert not serializer.is_valid()

        assert "new_password" in serializer.errors

    def test_password_validation_error(self, user):
        data = {"new_password": "short"}

        serializer = PasswordResetConfirmSerializer(data=data)

        assert not serializer.is_valid()

        assert "new_password" in serializer.errors
