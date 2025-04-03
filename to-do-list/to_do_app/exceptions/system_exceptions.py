from rest_framework import serializers
from rest_framework import exceptions


class OldPasswordIncorrect(serializers.ValidationError):
    default_detail = "Old password is not correct"


class PasswordsDontMatch(serializers.ValidationError):
    default_detail = "Password fields didn't match."


class EmailAlreadyExists(serializers.ValidationError):
    default_detail = "This email is already in use."


class UserNotFound(exceptions.NotFound):
    default_detail = "User with this email not found."


class AccountLocked(exceptions.PermissionDenied):
    default_detail = (
        "Your account has been locked due to too many failed login attempts."
    )
