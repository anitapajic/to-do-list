import pytest
from rest_framework import status
from unittest import mock


@pytest.mark.django_db
class TestPasswordResetView:
    def test_password_reset_invalid_email(self, api_client):
        password_reset_data = {"email": "nonexistent@example.com"}

        response = api_client.post("/api/users/password-reset/", password_reset_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "email" in response.data['error']['detail']

    def test_password_reset_missing_email(self, api_client):
        password_reset_data = {}

        response = api_client.post("/api/users/password-reset/", password_reset_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    @mock.patch("to_do_app.utils.send_password_reset_link.send_email")
    def test_password_reset_invalid_data(self, mock_send_email, api_client):
        password_reset_data = {"email": "invalid-email"}

        response = api_client.post("/api/users/password-reset/", password_reset_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

        mock_send_email.assert_not_called()
