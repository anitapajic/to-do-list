from django.apps import AppConfig


class ToDoAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "to_do_app"

    def ready(self):
        from to_do_app.utils.scheduler import start_scheduler

        start_scheduler()
