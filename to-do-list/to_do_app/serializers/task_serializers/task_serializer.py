from rest_framework import serializers
from to_do_app.models import Task


class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    subtasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "priority",
            "status",
            "category",
            "category_name",
            "parent",
            "subtasks",
            "created",
            "completed_at",
        ]
        extra_kwargs = {
            "category": {"write_only": True, "required": False},
            "description": {"required": False},
            "due_date": {"required": False},
            "priority": {"required": False},
            "status": {"required": False},
            "completed_at": {"required": False},
            "created": {"required": False},
        }

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
