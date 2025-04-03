import pytest
from unittest import mock
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator


@pytest.mark.django_db
class TestPasswordResetConfirmView:
    @pytest.fixture
    def valid_token(self, user):
        token_generator = PasswordResetTokenGenerator()
        return token_generator.make_token(user)

    def test_password_reset_confirm_success(self, api_client, user, valid_token):
        data = {"new_password": "NewValidPassword123!"}
        url = f"/api/users/password-reset-confirm/{user.id}/{valid_token}/"

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Password reset successful."

    def test_password_reset_confirm_invalid_token(self, api_client, user):
        invalid_token = "invalidtoken123"
        data = {"new_password": "NewValidPassword123!"}
        url = f"/api/users/password-reset-confirm/{user.id}/{invalid_token}/"

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["detail"] == "Invalid or expired token."

    def test_password_reset_confirm_invalid_password(
        self, api_client, user, valid_token
    ):
        data = {"new_password": "short"}
        url = f"/api/users/password-reset-confirm/{user.id}/{valid_token}/"

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "new_password" in response.data

    def test_password_reset_confirm_missing_password(
        self, api_client, valid_token, user
    ):
        data = {}
        url = f"/api/users/password-reset-confirm/{user.id}/{valid_token}/"

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "new_password" in response.data

    @mock.patch("django.contrib.auth.tokens.PasswordResetTokenGenerator.check_token")
    def test_password_reset_confirm_token_check(
        self, mock_check_token, api_client, user, valid_token
    ):
        mock_check_token.return_value = False
        data = {"new_password": "NewValidPassword123!"}
        url = f"/api/users/password-reset-confirm/{user.id}/{valid_token}/"

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["detail"] == "Invalid or expired token."
