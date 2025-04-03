from django.db import models
from django.utils import timezone
from .enums.task_status import TaskStatus
from .enums.priority import Priority
from .user import User
from .category import Category
from .base_model import BaseModel


class Task(BaseModel):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=255, null=True)
    due_date = models.DateTimeField(null=True)
    priority = models.CharField(
        max_length=15, choices=Priority.choices(), default=Priority.LOW.value
    )
    status = models.CharField(
        max_length=15, choices=TaskStatus.choices(), default=TaskStatus.PENDING.value
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="subtasks"
    )

    class Meta:
        ordering = ["created"]
    
    def save(self, *args, **kwargs):
        if self.status == TaskStatus.COMPLETED.value and self.completed_at is None:
            self.completed_at = timezone.now()
        elif self.status != TaskStatus.COMPLETED.value:
            self.completed_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
