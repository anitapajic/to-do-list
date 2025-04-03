from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )

    def save(self, user):
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
