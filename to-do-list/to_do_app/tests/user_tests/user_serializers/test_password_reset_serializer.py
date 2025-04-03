import pytest
from unittest import mock
from to_do_app.serializers.user_serializers.password_reset_serializer import (
    PasswordResetSerializer,
)
from to_do_app.exceptions.system_exceptions import UserNotFound


@pytest.mark.django_db
class TestPasswordResetSerializer:
    @pytest.fixture
    def password_reset_data(self):
        return {
            "email": "testuser@example.com",
        }

    def test_valid_email_for_password_reset(self, user, password_reset_data):
        serializer = PasswordResetSerializer(data=password_reset_data)
        assert serializer.is_valid()

        reset_link = serializer.save()

        assert reset_link is not None
        assert reset_link.startswith("http://")
        assert "user" in serializer.context
        assert serializer.context["user"] == user

    def test_invalid_email_for_password_reset(self, password_reset_data):
        password_reset_data["email"] = "nonexistent@example.com"

        serializer = PasswordResetSerializer(data=password_reset_data)

        with pytest.raises(UserNotFound):
            serializer.is_valid(raise_exception=True)

    @mock.patch("django.contrib.auth.tokens.PasswordResetTokenGenerator.make_token")
    @mock.patch("to_do_app.utils.send_password_reset_link.send_email")
    def test_reset_link_with_token_generation(
        self, mock_send_email, mock_make_token, user, password_reset_data
    ):
        mock_make_token.return_value = "fake-token"

        serializer = PasswordResetSerializer(data=password_reset_data)
        assert serializer.is_valid()

        reset_link = serializer.save()

        assert "fake-token" in reset_link

    def test_no_user_found_on_invalid_email(self):
        invalid_email = "invaliduser@example.com"
        serializer = PasswordResetSerializer(data={"email": invalid_email})

        with pytest.raises(UserNotFound):
            serializer.is_valid(raise_exception=True)
