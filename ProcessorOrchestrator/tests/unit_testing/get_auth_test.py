"""

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

Unit testing module that only tests tracking object class.
"""

import os
from src.get_auth import get_auth_params


def test_auth_creation_without_environment_returns_null():
    """Test if getting auth parameters when the environment isn't set returns None"""
    null_client, null_processor = get_auth_params()
    assert null_client is None
    assert null_processor is None


def test_auth_creation_with_partial_environment_returns_null():
    """Test if setting the environment only partially still returns null"""
    os.environ["PUBLIC_KEY"] = "/app/tests/unit_testing/files/key.pem"
    os.environ["AUDIENCE"] = "aud"

    null_client, null_processor = get_auth_params()
    assert null_client is None
    assert null_processor is None

    del os.environ["PUBLIC_KEY"]
    del os.environ["AUDIENCE"]


def test_auth_creation_with_environment_creates_valid_auth():
    """Test if setting the environment and then getting auth parameters creates the proper
    Auth object"""
    os.environ["PUBLIC_KEY"] = "/app/tests/unit_testing/files/key.pem"
    os.environ["AUDIENCE"] = "aud"
    os.environ["CLIENT_ROLE"] = "cl_role"
    os.environ["PROCESSOR_ROLE"] = "pr_role"

    client_auth, processor_auth = get_auth_params()

    assert client_auth.audience == "aud"
    assert processor_auth.audience == "aud"
    assert client_auth.role == "cl_role"
    assert processor_auth.role == "pr_role"

    del os.environ["PUBLIC_KEY"]
    del os.environ["AUDIENCE"]
    del os.environ["CLIENT_ROLE"]
    del os.environ["PROCESSOR_ROLE"]
