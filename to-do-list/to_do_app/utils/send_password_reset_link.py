from django.core.mail import send_mail
from django.template.loader import render_to_string
from to_do_app.models.user import User
from to_do_app.decorators.email_enabled import email_enabled


@email_enabled
def send_email(user: User, reset_link: str):
    subject = "To Do App: Password reset link"
    recipient = user.email
    context = {
        "user": user,
        "reset_link": reset_link,
    }
    message = render_to_string("to_do_app/password_reset_email.html", context)
    send_mail(
        subject,
        "",
        "",
        [recipient],
        html_message=message,
    )
