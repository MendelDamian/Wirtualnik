from typing import Callable

import pytest
from django.forms.models import model_to_dict
from rest_framework.test import APIClient

from backend.users.models import User
from backend.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def make_user() -> Callable[..., User]:
    def make(**kwargs) -> User:
        return UserFactory(**kwargs)

    return make


@pytest.fixture
def build_user() -> Callable[..., dict[str, any]]:
    def make(**kwargs) -> dict[str, any]:
        return model_to_dict(UserFactory.build(**kwargs))

    return make
