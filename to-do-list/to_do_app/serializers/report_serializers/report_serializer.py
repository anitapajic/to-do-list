from rest_framework import serializers


class ReportSerializer(serializers.Serializer):
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    overdue_percentage = serializers.FloatField()
    avg_completion_time_hours = serializers.FloatField()
