from typing import Callable

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import User

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


def test_detail_view_with_soft_deleted_user(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    user = make_user()
    user.delete()

    url = reverse("user-detail", kwargs={"uuid": user.uuid})
    response = api_client.get(path=url)
    assert response.status_code == 404


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

    user = make_user(**old_data)

    url = reverse("user-detail", kwargs={"uuid": user.uuid})
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

    response = api_client.put(path=url, data=new_data)
    assert response.status_code == 200

    data = response.json()
    assert data.get('first_name') == new_data.get('first_name')
    assert data.get('last_name') == new_data.get('last_name')
    assert data.get('email') == new_data.get('email')


def test_update_view_with_invalid_data(
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
        "email": "invalid",
    }

    user = make_user(**old_data)
    url = reverse("user-detail", kwargs={"uuid": user.uuid})
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

    response = api_client.put(path=url, data=new_data)
    assert response.status_code == 400


def test_update_view_with_password(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    old_data = {
        "password": "0ld_P@$$w0rD",
    }

    new_data = {
        "password": "N3w_P@$$w0rD",
    }

    user = make_user(**old_data)
    url = reverse("user-detail", kwargs={"uuid": user.uuid})
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

    response = api_client.put(path=url, data=new_data)
    assert response.status_code == 200

    user.refresh_from_db()
    assert user.check_password(new_data.get('password')) is False


def test_update_view_with_invalid_token(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    user = make_user(first_name="old_first_name")
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


def test_update_view_with_soft_deleted_user(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    user = make_user()
    user.delete()

    url = reverse("user-detail", kwargs={"uuid": user.uuid})
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

    response = api_client.put(path=url, data={"first_name": "new_first_name"})
    assert response.status_code == 404


def test_create_view_with_valid_data(
    api_client: APIClient,
):
    data = {
        "username": "new_username",
        "password": "p@$$w0rD",
        "first_name": "new_first_name",
        "last_name": "new_last_name",
        "email": "new_email@example.com",
    }

    url = reverse("user-list")
    response = api_client.post(path=url, data=data)
    assert response.status_code == 201

    response_data = response.json()
    assert response_data.get('username') == data.get('username')
    assert response_data.get('first_name') == data.get('first_name')
    assert response_data.get('last_name') == data.get('last_name')
    assert response_data.get('email') == data.get('email')

    user = User.objects.first()
    assert user.username == data.get('username')
    assert user.first_name == data.get('first_name')
    assert user.last_name == data.get('last_name')
    assert user.email == data.get('email')
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.is_active is True
    assert user.check_password(data.get('password')) is True


def test_create_view_with_missing_password(
    api_client: APIClient,
):
    data = {
        "username": "new_username",
        # "password": "p@$$w0rD",
        "first_name": "new_first_name",
        "last_name": "new_last_name",
        "email": "new_email@example.com",
    }

    url = reverse("user-list")
    response = api_client.post(path=url, data=data)
    assert response.status_code == 400


def test_create_view_with_missing_username(
    api_client: APIClient,
):
    data = {
        # "username": "new_username",
        "password": "p@$$w0rD",
        "first_name": "new_first_name",
        "last_name": "new_last_name",
        "email": "new_email@example.com",
    }

    url = reverse("user-list")
    response = api_client.post(path=url, data=data)
    assert response.status_code == 400


def test_create_view_with_invalid_email(
    api_client: APIClient,
):
    data = {
        "username": "new_username",
        "password": "p@$$w0rD",
        "first_name": "new_first_name",
        "last_name": "new_last_name",
        "email": "invalid",
    }

    url = reverse("user-list")
    response = api_client.post(path=url, data=data)
    assert response.status_code == 400


def test_create_view_with_forbidden_fields(
    api_client: APIClient,
):
    data = {
        "username": "new_username",
        "password": "p@$$w0rD",
        "first_name": "new_first_name",
        "last_name": "new_last_name",
        "email": "new_email@example.com",
        "is_staff": True,
        "is_superuser": True,
        "uuid": "some_uuid",
    }

    url = reverse("user-list")
    response = api_client.post(path=url, data=data)
    assert response.status_code == 201

    user = User.objects.first()
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.uuid is not data.get('uuid')


def test_create_view_with_already_existing_username(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    data = {
        "username": "some_username",
    }

    make_user(**data)
    url = reverse("user-list")
    response = api_client.post(path=url, data=data)
    assert response.status_code == 400


def test_create_view_with_same_username_as_soft_deleted_user(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    """
    This test is to ensure that the user is not created if the username is
    already taken by a soft deleted user. This is to prevent the user from
    being restored and to keep data clean.
    """
    data = {
        "username": "some_username",
        "password": "p@$$w0rD",
    }

    user = make_user(**data)
    user.delete()

    url = reverse("user-list")
    response = api_client.post(path=url, data=data)
    assert response.status_code == 400


def test_destroy_view_with_valid_token(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    user = make_user()
    url = reverse("user-detail", kwargs={"uuid": user.uuid})
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

    response = api_client.delete(path=url)
    assert response.status_code == 204

    assert User.available_objects.count() == 0
    assert User.objects.count() == 1


def test_destroy_view_with_invalid_token(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    user = make_user()
    url = reverse("user-detail", kwargs={"uuid": user.uuid})
    api_client.credentials(HTTP_AUTHORIZATION=f"Token invalid")

    response = api_client.delete(path=url)
    assert response.status_code == 403


def test_destroy_view_with_already_soft_deleted_user(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    user = make_user()
    user.delete()

    url = reverse("user-detail", kwargs={"uuid": user.uuid})
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

    response = api_client.delete(path=url)
    assert response.status_code == 404


def test_update_password_view_with_valid_token(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    data = {
        "old_password": "0ld_p@$$w0rD",
        "new_password": "N3w_p@$$w0rD",
    }

    user = make_user(password=data.get("old_password"))
    url = reverse("change-password")
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

    response = api_client.put(path=url, data=data)
    assert response.status_code == 204

    user.refresh_from_db()
    assert user.check_password(data.get('new_password')) is True


def test_update_password_view_with_invalid_token(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    data = {
        "old_password": "0ld_p@$$w0rD",
        "new_password": "N3w_p@$$w0rD",
    }

    make_user(password=data.get("old_password"))
    url = reverse("change-password")
    api_client.credentials(HTTP_AUTHORIZATION=f"Token invalid")

    response = api_client.put(path=url, data=data)
    assert response.status_code == 403


def test_update_password_view_with_invalid_old_password(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    data = {
        "old_password": "1nc0r3cT_p@$$w0rD",
        "new_password": "N3w_p@$$w0rD",
    }

    user = make_user(password="W31Rd_p@$$w0rD")
    url = reverse("change-password")
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

    response = api_client.put(path=url, data=data)
    assert response.status_code == 400


def test_update_password_view_with_empty_data(
    make_user: Callable[..., User],
    api_client: APIClient,
):
    user = make_user()
    url = reverse("change-password")
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

    response = api_client.put(path=url, data={})
    assert response.status_code == 400
