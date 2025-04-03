from enum import Enum


class Priority(Enum):
    LOW =  "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

    @classmethod
    def choices(cls):
        return [(priority.value, priority.name) for priority in cls]
