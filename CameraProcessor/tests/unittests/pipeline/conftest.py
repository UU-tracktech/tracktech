"""Conftest file for pipeline.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import pytest
from tests.unittests.utils.fake_websocket import FakeWebsocket

# Can't use None client because Docker dislikes using windows
# @pytest.fixture(params=[FakeWebsocket(), None], ids=["Fake Client", "None Client"])
# def clients(request):
#     return request.param


@pytest.fixture(params=[FakeWebsocket()], ids=["Fake Client"])
def clients(request):
    """Fixture for a couple of clients

    Returns:
        A fake websocket client

    """
    return request.param
