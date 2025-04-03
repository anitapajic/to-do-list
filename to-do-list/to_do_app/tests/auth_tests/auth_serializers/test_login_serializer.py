import pytest
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from to_do_app.serializers.auth_serializers.login_serializer import LoginSerializer
from to_do_app.models.enums.role import Role


@pytest.mark.django_db
class TestLoginSerializer:
    def test_get_token_includes_email_and_role(self, user):
        token = LoginSerializer.get_token(user)

        token_dict = token.payload

        assert "email" in token_dict
        assert token_dict["email"] == "testuser@example.com"
        assert "role" in token_dict
        assert token_dict["role"] == Role.USER.value

        assert "exp" in token_dict
        assert "iat" in token_dict
        assert "user_id" in token_dict

    def test_token_with_different_role(self, user):
        user.role = Role.ADMIN.value
        user.save()

        token = LoginSerializer.get_token(user)
        token_dict = token.payload

        assert "role" in token_dict
        assert token_dict["role"] == Role.ADMIN.value
        assert token_dict["email"] == "testuser@example.com"

    def test_parent_token_behavior_preserved(self, user):
        base_token = TokenObtainPairSerializer.get_token(user)
        custom_token = LoginSerializer.get_token(user)

        base_dict = base_token.payload
        custom_dict = custom_token.payload

        assert base_dict["exp"] == custom_dict["exp"]
        assert base_dict["iat"] == custom_dict["iat"]
        assert base_dict["user_id"] == custom_dict["user_id"]

        assert "email" in custom_dict
        assert "role" in custom_dict
        assert "email" not in base_dict
        assert "role" not in base_dict

    def test_token_with_custom_user_fields(self, user):
        user.name = "Test Name"
        user.save()

        token = LoginSerializer.get_token(user)
        token_dict = token.payload

        assert "email" in token_dict
        assert "role" in token_dict
        assert "name" not in token_dict
