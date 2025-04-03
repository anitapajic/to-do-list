from rest_framework.permissions import BasePermission
from to_do_app.models.enums.role import Role

class IsTaskOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.ADMIN.value
