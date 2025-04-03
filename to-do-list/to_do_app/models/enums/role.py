from enum import Enum


class Role(Enum):
    USER = "user"
    ADMIN = "Admin"

    @classmethod
    def choices(cls):
        return [(role.value, role.name) for role in cls]
