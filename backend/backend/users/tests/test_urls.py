import uuid
from contextlib import contextmanager

import pytest
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize(
    "example_input,kwargs,expectation",
    [
        ("users:user-list", {}, does_not_raise()),
        ("users:user-detail", {"uuid": str(uuid.uuid4())}, does_not_raise()),
        ("users:change-password", {}, does_not_raise()),

        ("users:user-list", {"uuid": str(uuid.uuid4())}, pytest.raises(NoReverseMatch)),
        ("users:user-detail", {}, pytest.raises(NoReverseMatch)),
    ],
)
def test_urls_generated_successfully(example_input, kwargs, expectation):
    """
    Test that all URLs are generated successfully.
    """
    with expectation:
        assert reverse(example_input, kwargs=kwargs) is not None
