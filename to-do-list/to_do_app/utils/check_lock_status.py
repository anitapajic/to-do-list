import logging
from to_do_app.exceptions.system_exceptions import AccountLocked

logger = logging.getLogger(__name__)


def check_lock_status(user):
    if user and user.is_lock_expired():
        user.unlock_account()
        logger.info(f"Account unlocked automatically after 24h: {user.email}")
    elif user and user.is_locked:
        logger.warning(f"Locked account login attempt: {user.email}")
        raise AccountLocked()
