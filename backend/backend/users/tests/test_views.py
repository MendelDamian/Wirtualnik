from typing import Callable

import pytest
from django.urls import reverse
# from django.test import Client
from rest_framework.test import APIClient

from backend.users.models import User

pytestmark = pytest.mark.django_db


def test_detail_view_with_valid_uuid(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    user = make_user()
    url = reverse("user-detail", kwargs={"uuid": user.uuid})
    response = api_client.get(path=url)
    assert response.status_code == 200

    data = response.json()
    assert data.get('uuid') == str(user.uuid)


def test_detail_view_with_invalid_uuid(
    api_client: APIClient,
):
    url = reverse("user-detail", kwargs={"uuid": "invalid"})
    response = api_client.get(path=url)
    assert response.status_code == 404


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


def test_update_view_with_valid_uuid(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    old_data = {
        "first_name": "old_first_name",
        "last_name": "old_last_name",
        "email": "old_email@example.com",
    }

    new_data = {
        "first_name": "new_first_name",
        "last_name": "new_last_name",
        "email": "new_email@example.com",
    }

    make_user(**old_data)
    user = User.objects.first()

    url = reverse("user-detail", kwargs={"uuid": user.uuid})
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

    response = api_client.put(path=url, data=new_data)
    assert response.status_code == 200

    data = response.json()
    assert data.get('first_name') == new_data.get('first_name')
    assert data.get('last_name') == new_data.get('last_name')
    assert data.get('email') == new_data.get('email')


def test_update_view_with_invalid_token(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    make_user(first_name="old_first_name")
    user = User.objects.first()

    url = reverse("user-detail", kwargs={"uuid": user.uuid})
    api_client.credentials(HTTP_AUTHORIZATION=f"Token invalid")

    response = api_client.put(path=url, data={"first_name": "new_first_name"})
    assert response.status_code == 403


def test_update_view_with_invalid_uuid(
    api_client: APIClient,
):
    url = reverse("user-detail", kwargs={"uuid": "invalid"})
    response = api_client.put(path=url, data={"first_name": "new_first_name"})
    assert response.status_code == 404
