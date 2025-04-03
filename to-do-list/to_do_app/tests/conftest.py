import pytest
from rest_framework.test import APIClient
from to_do_app.tests.factories import UserFactory, CategoryFactory
from to_do_app.models.enums.role import Role

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory(email="testuser@example.com", role=Role.USER.value, is_active=True)


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def category(db):
    return CategoryFactory()


@pytest.fixture
def category_list(db):
    return CategoryFactory.create_batch(5)
