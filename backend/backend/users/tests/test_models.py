from typing import Callable

import pytest
from rest_framework.authtoken.models import Token

from backend.users.models import User

pytestmark = pytest.mark.django_db


def test_model_with_creating_token_on_save(
    make_user: Callable[..., User],
):
    assert Token.objects.count() == 0
    make_user()
    assert Token.objects.count() == 1


def test_model_with_creating_user_with_taken_username(
    make_user: Callable[..., User],
):
    username = "test_user"

    user = make_user(username=username)
    assert User.objects.count() == 1
    assert str(user) == username

    make_user(username=username)
    assert User.objects.count() == 1
