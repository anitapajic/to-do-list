from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from to_do_app.models.user import User
from to_do_app.exceptions.system_exceptions import UserNotFound
from to_do_app.utils.send_password_reset_link import send_email
from urllib.parse import urljoin
import os

TOKEN_URL = os.getenv("PASSWORD_RESET_CONFIRM_URL")


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise UserNotFound()

        self.context["user"] = user
        return value

    def save(self):
        user = self.context["user"]
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        reset_link = urljoin(TOKEN_URL, f"{user.id}/{token}/")

        send_email(user, reset_link)

        return reset_link
