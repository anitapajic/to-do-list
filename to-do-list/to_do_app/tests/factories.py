import factory
from to_do_app.models.category import Category
from to_do_app.models.user import User
from to_do_app.models.task import Task
from to_do_app.models.enums.role import Role
from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    role = factory.LazyAttribute(lambda _: Role.USER.value)
    password = factory.PostGenerationMethodCall("set_password", "Test1234!")
    failed_login_attempts = 0
    is_locked = False
    locked_at = None


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    owner = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=3)
    due_date = factory.LazyFunction(lambda: timezone.now())

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        created = kwargs.pop("created", timezone.now())
        obj = model_class(*args, **kwargs)
        obj.save()
        obj.created = created
        obj.save(update_fields=["created"])
        return obj
