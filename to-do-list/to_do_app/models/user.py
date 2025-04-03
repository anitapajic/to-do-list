from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta
from to_do_app.managers.custom_user_manager import CustomUserManager
from .enums.role import Role
from .base_model import BaseModel


class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(unique=True, null=False)
    name = models.CharField(max_length=50, null=False)
    role = models.CharField(
        max_length=15, choices=Role.choices(), default=Role.USER.value
    )
    failed_login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def lock_account(self):
        self.is_locked = True
        self.locked_at = now()
        self.failed_login_attempts = 4
        self.save(update_fields=['is_locked', 'locked_at', 'failed_login_attempts'])

    def unlock_account(self):
        self.is_locked = False
        self.failed_login_attempts = 0
        self.locked_at = None
        self.save(update_fields=['is_locked', 'failed_login_attempts', 'locked_at'])

    def is_lock_expired(self):
        return self.is_locked and self.locked_at and now() > self.locked_at + timedelta(hours=24)
