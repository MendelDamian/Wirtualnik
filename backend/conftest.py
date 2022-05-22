import pytest
from rest_framework.test import APIClient

pytest_plugins = ('backend.users',)


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
