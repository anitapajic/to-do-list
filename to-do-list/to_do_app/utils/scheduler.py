from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta
from django.utils import timezone
from to_do_app.models import Task
from to_do_app.utils.send_task_reminders import send_email
from to_do_app.utils.datetime_utils import (
    create_midnight_datetime,
    create_microsecond_to_midnight,
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_due_date_reminders():
    current_time = timezone.now()
    today_start = create_midnight_datetime(current_time)
    tomorrow_end = create_microsecond_to_midnight(current_time + timedelta(days=1))

    tasks = Task.objects.filter(due_date__range=(today_start, tomorrow_end))

    for task in tasks:
        send_email(task)

    logger.info(f"Sent {tasks.count()} due date reminders.")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_due_date_reminders, "cron", hour=10, minute=35)
    scheduler.start()
    logger.info("Scheduler started!")
