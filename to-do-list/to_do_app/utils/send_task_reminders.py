from django.core.mail import send_mail
from django.template.loader import render_to_string
from to_do_app.models.task import Task
from to_do_app.decorators.email_enabled import email_enabled


@email_enabled
def send_email(task: Task):
    subject = "Reminder: Task Due Date Approaching"
    recipient = task.owner.email
    context = {
        "name": task.owner.name,
        "taskName": task.title,
        "dueDate": task.due_date.strftime("%d-%m-%Y"),
    }
    message = render_to_string("to_do_app/due_date_email.html", context)
    send_mail(
        subject,
        "",
        "",
        [recipient],
        html_message=message,
    )
