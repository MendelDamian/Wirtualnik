from typing import Callable

import pytest
from rest_framework.test import APIClient

from backend.users.models import User

pytestmark = pytest.mark.django_db


def test_api_auth_token_with_valid_data(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    user = make_user(password="p@ssw0rd")
    response = api_client.post(path='/api-token-auth/', data={"username": user.username, "password": "p@ssw0rd"})
    assert response.status_code == 200

    data = response.json()
    assert data.get("token") is not None


def test_api_auth_token_with_invalid_data(
    api_client: APIClient,
):
    response = api_client.post(path='/api-token-auth/', data={"username": "invalid", "password": "invalid"})
    assert response.status_code == 400
