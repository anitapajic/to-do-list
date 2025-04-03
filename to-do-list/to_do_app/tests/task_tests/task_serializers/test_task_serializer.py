import pytest
from rest_framework.exceptions import ValidationError
from to_do_app.serializers.task_serializers.task_serializer import TaskSerializer
from to_do_app.tests.factories import TaskFactory, CategoryFactory
from to_do_app.models.enums.task_status import TaskStatus


@pytest.mark.django_db
class TestTaskSerializer:
    def test_task_serializer_valid(self, user, category):
        task = TaskFactory(owner=user, category=category)
        data = {
             "title": "Test Task",
             "owner": user.id,
             "category": category.id
        }

        serializer = TaskSerializer(instance=task, data=data)
        assert serializer.is_valid()
        assert serializer.data["id"] == str(task.id)
        assert serializer.data["title"] == task.title
        assert serializer.data["category_name"] == category.name
        assert serializer.data["subtasks"] == []
        assert serializer.data["parent"] is None

    def test_task_serializer_category_name(self):
        category = CategoryFactory(name="Test Category")
        task = TaskFactory(category=category)

        serializer = TaskSerializer(task)
        assert serializer.data["category_name"] == "Test Category"

    def test_task_serializer_without_category(self):
        task = TaskFactory(category=None)

        serializer = TaskSerializer(task)
        assert serializer.data["category_name"] is None

    def test_task_serializer_with_subtasks(self, user, category):
        parent_task = TaskFactory(owner=user, category=category)
        subtask = TaskFactory(owner=user, parent=parent_task)

        serializer = TaskSerializer(parent_task)
        assert "subtasks" in serializer.data
        assert len(serializer.data["subtasks"]) == 1
        assert serializer.data["subtasks"][0] == subtask.id

    def test_task_serializer_with_parent(self, user, category):
        parent_task = TaskFactory(owner=user, category=category)
        task = TaskFactory(owner=user, category=category, parent=parent_task)

        serializer = TaskSerializer(task)
        assert serializer.data["parent"] == parent_task.id

    def test_task_serializer_optional_fields(self):
        task = TaskFactory(
            description="Test Description", priority=3, status=TaskStatus.IN_PROGRESS.value
        )

        serializer = TaskSerializer(task)
        assert serializer.data["description"] == "Test Description"
        assert serializer.data["priority"] == 3
        assert serializer.data["status"] == TaskStatus.IN_PROGRESS.value
        assert "due_date" in serializer.data

    def test_task_serializer_missing_required_fields(self):
        task = TaskFactory()
        data = {}

        serializer = TaskSerializer(instance=task, data=data)
        assert not serializer.is_valid()
        assert "title" in serializer.errors
        assert "This field is required." in str(serializer.errors["title"])

    def test_task_serializer_invalid_parent(self, user, category):
        invalid_parent_id = 999
        data = {
            "title": "Test Task",
            "category": category.id,
            "owner": user.id,
            "parent": invalid_parent_id,
        }

        serializer = TaskSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_task_serializer_create_task(self, user, category):
        task = TaskFactory(title= "Test Task", owner=user, category=category)

        data = {
            "title": task.title,
            "category": category.id,
            "owner": user.id,
        }

        serializer = TaskSerializer(instance=task, data=data)
        assert serializer.is_valid()
        task = serializer.save()
        assert task.id is not None
        assert task.owner == user
        assert task.category == category
        assert task.title == "Test Task"
