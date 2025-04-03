from enum import Enum


class TaskStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"

    @classmethod
    def choices(cls):
        return [(status.value, status.name) for status in cls]
