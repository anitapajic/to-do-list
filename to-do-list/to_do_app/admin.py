from django.contrib import admin
from .models.user import User
from .models.category import Category
from .models.task import Task

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Task)
