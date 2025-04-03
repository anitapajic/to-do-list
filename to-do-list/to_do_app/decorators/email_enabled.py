from functools import wraps
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def email_enabled(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        required_settings = [
            "EMAIL_BACKEND",
            "EMAIL_HOST",
            "EMAIL_HOST_USER",
            "EMAIL_HOST_PASSWORD",
            "EMAIL_PORT",
            "DEFAULT_FROM_EMAIL",
        ]

        if missing_settings := [
            s for s in required_settings if not getattr(settings, s, None)
        ]:
            logger.warning(
                f"Email settings are missing: {', '.join(missing_settings)}. Skipping email send."
            )
            return

        return func(*args, **kwargs)

    return wrapper
