from rest_framework import serializers
from to_do_app.models.user import User
from to_do_app.exceptions.system_exceptions import EmailAlreadyExists


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ("id", "email", "name")

    def validate_email(self, value):
        user = self.instance
        if user and User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise EmailAlreadyExists()
        return value
