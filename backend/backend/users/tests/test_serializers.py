from typing import Callable

import pytest
from django.contrib.auth.hashers import check_password

from ..serializers import CreateUserSerializer

pytestmark = pytest.mark.django_db


def test_serializer_with_empty_data():
    serializer = CreateUserSerializer(data={})
    assert serializer.is_valid() is False


def test_serializer_with_valid_data(build_user: Callable[..., dict[str, any]]):
    user_data = {
        "username": "test_user",
        "first_name": "Test_first_name",
        "last_name": "Test_last_name",
        "email": "test@example.com"
    }
    serializer = CreateUserSerializer(data=build_user(**user_data))
    assert serializer.is_valid() is True

    user = serializer.save()
    assert user.username == user_data["username"]
    assert user.first_name == user_data["first_name"]
    assert user.last_name == user_data["last_name"]
    assert user.email == user_data["email"]


def test_serializer_hashes_password(build_user: Callable[..., dict[str, any]]):
    user_data = build_user()
    serializer = CreateUserSerializer(data=user_data)
    assert serializer.is_valid() is True

    user = serializer.save()
    assert check_password(user_data.get("password"), user.password) is True
