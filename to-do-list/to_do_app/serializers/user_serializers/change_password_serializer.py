from rest_framework import serializers
from rest_framework import exceptions
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from to_do_app.models.user import User
from to_do_app.exceptions.system_exceptions import (
    OldPasswordIncorrect,
    PasswordsDontMatch,
)


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise PasswordsDontMatch()

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise OldPasswordIncorrect()
        return value

    def update(self, instance, validated_data):
        user = self.context["request"].user

        if user.pk != instance.pk:
            raise exceptions.PermissionDenied(
                "You dont have permission for this user.",
                code=status.HTTP_403_FORBIDDEN,
            )

        instance.set_password(validated_data["password"])
        instance.save()

        return instance
