import pytest
from django.urls import reverse
from rest_framework import status
from to_do_app.tests.factories import CategoryFactory


@pytest.mark.django_db
def test_list_categories(authenticated_client, category_list):
    url = reverse("category-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(category_list)


@pytest.mark.django_db
def test_create_category(authenticated_client):
    url = reverse("category-list")
    data = {"name": "New Category"}
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert CategoryFactory._meta.model.objects.filter(name="New Category").exists()


@pytest.mark.django_db
def test_update_category(authenticated_client, category):
    url = reverse("category-detail", kwargs={"pk": category.id})
    data = {"name": "Updated Category"}
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    category.refresh_from_db()
    assert category.name == "Updated Category"


@pytest.mark.django_db
def test_delete_category(authenticated_client, category):
    url = reverse("category-detail", kwargs={"pk": category.id})
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not CategoryFactory._meta.model.objects.filter(id=category.id).exists()


@pytest.mark.django_db
def test_unauthenticated_user_cannot_access(api_client):
    url = reverse("category-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_category_with_null_name(authenticated_client):
    url = reverse("category-list")
    data = {"name": None}
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data or "error" in response.data


@pytest.mark.django_db
def test_create_category_with_too_long_name(authenticated_client):
    url = reverse("category-list")
    data = {"name": "A" * 101}
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data or "error" in response.data
