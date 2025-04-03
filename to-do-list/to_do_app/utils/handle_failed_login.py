import logging
import os
from to_do_app.exceptions.system_exceptions import AccountLocked

logger = logging.getLogger(__name__)


def handle_failed_login(user):
    user.failed_login_attempts += 1
    if user.failed_login_attempts >= int(os.getenv("MAX_LOGIN_FAILED_ATTEMPTS")):
        user.lock_account()
        logger.warning(f"User account locked: {user.email}")
        raise AccountLocked()
    else:
        user.save(update_fields=["failed_login_attempts"])
        logger.info(f"Failed attempts updated to: {user.failed_login_attempts}")
