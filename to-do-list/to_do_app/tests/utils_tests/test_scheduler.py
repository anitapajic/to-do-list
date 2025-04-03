from to_do_app.tests.factories import TaskFactory
from to_do_app.utils.scheduler import send_due_date_reminders
from unittest.mock import patch
from django.utils import timezone
from datetime import timedelta


def test_send_due_date_reminders_today_task(db):
    reference_time = timezone.now().replace(microsecond=0)
    today_task = TaskFactory(
        due_date=reference_time.replace(hour=9, minute=0, second=0)
    )

    with patch("to_do_app.utils.scheduler.send_email") as mock_send_email:
        with patch("django.utils.timezone.now", return_value=reference_time):
            send_due_date_reminders()
        mock_send_email.assert_called_once_with(today_task)


def test_send_due_date_reminders_future_task(db):
    reference_time = timezone.now().replace(microsecond=0)
    tomorrow = reference_time + timedelta(days=1)
    future_task = TaskFactory(due_date=tomorrow.replace(hour=10, minute=0, second=0))

    with patch("to_do_app.utils.scheduler.send_email") as mock_send_email:
        with patch("django.utils.timezone.now", return_value=reference_time):
            send_due_date_reminders()
        mock_send_email.assert_called_once_with(future_task)


def test_send_due_date_reminders_past_task(db):
    reference_time = timezone.now().replace(microsecond=0)
    past_task = TaskFactory(due_date=reference_time.replace(hour=7, minute=0, second=0))

    with patch("to_do_app.utils.scheduler.send_email") as mock_send_email:
        with patch("django.utils.timezone.now", return_value=reference_time):
            send_due_date_reminders()
        mock_send_email.assert_called_once_with(past_task)


def test_send_due_date_reminders_no_tasks(db):
    reference_time = timezone.now().replace(microsecond=0)
    with patch("to_do_app.utils.scheduler.send_email") as mock_send_email:
        with patch("django.utils.timezone.now", return_value=reference_time):
            send_due_date_reminders()
        mock_send_email.assert_not_called()


def test_send_due_date_reminders_multiple_tasks(db):
    reference_time = timezone.now().replace(microsecond=0)
    task1 = TaskFactory(due_date=reference_time.replace(hour=9, minute=0, second=0))
    tomorrow = reference_time + timedelta(days=1)
    task2 = TaskFactory(due_date=tomorrow.replace(hour=10, minute=0, second=0))
    task3 = TaskFactory(due_date=reference_time.replace(hour=7, minute=0, second=0))

    with patch("to_do_app.utils.scheduler.send_email") as mock_send_email:
        with patch("django.utils.timezone.now", return_value=reference_time):
            send_due_date_reminders()

        assert mock_send_email.call_count == 3
        called_tasks = {call.args[0] for call in mock_send_email.call_args_list}
        assert task1 in called_tasks
        assert task2 in called_tasks
        assert task3 in called_tasks
