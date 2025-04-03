import pytest
from to_do_app.serializers.report_serializers.report_serializer import ReportSerializer


@pytest.fixture
def test_data():
    return {
        "total_tasks": 10,
        "completed_tasks": 5,
        "overdue_percentage": 20.5,
        "avg_completion_time_hours": 24.75,
    }


@pytest.mark.django_db
class TestReportSerializer:
    def test_valid_serialization(self, test_data):
        serializer = ReportSerializer(data=test_data)
        assert serializer.is_valid()
        assert serializer.validated_data == test_data
        assert serializer.data == test_data

    def test_missing_field_validation(self, test_data):
        test_data.pop("completed_tasks")

        serializer = ReportSerializer(data=test_data)
        assert not serializer.is_valid()
        assert "completed_tasks" in serializer.errors

    def test_invalid_field_types(self, test_data):
        test_data["total_tasks"] = "not_an_integer"
        test_data["overdue_percentage"] = "not_a_float"

        serializer = ReportSerializer(data=test_data)
        assert not serializer.is_valid()
        assert "total_tasks" in serializer.errors
        assert "overdue_percentage" in serializer.errors
