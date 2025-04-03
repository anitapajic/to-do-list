import pytest
from to_do_app.serializers.category_serializers.category_serializer import (
    CategorySerializer,
)


@pytest.mark.django_db
def test_category_serializer_valid_data(category):
    serializer = CategorySerializer(instance=category)
    data = serializer.data
    assert "id" in data
    assert "name" in data
    assert data["name"] == category.name


@pytest.mark.django_db
def test_category_serializer_invalid_null_name():
    data = {"name": None}
    serializer = CategorySerializer(data=data)
    assert not serializer.is_valid()
    assert "name" in serializer.errors


@pytest.mark.django_db
def test_category_serializer_invalid_long_name():
    data = {"name": "A" * 101}  
    serializer = CategorySerializer(data=data)
    assert not serializer.is_valid()
    assert "name" in serializer.errors
