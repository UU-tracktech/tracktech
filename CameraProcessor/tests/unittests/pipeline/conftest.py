"""The conftest file for the pipeline.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest
from tests.unittests.utils.fake_websocket import FakeWebsocket


@pytest.fixture(params=[FakeWebsocket()], ids=['Fake Client'])
def clients(request):
    """Fixture for a couple of clients.

    Args:
        request ([FakeWebsocket]): Fake WebSocket implementation.

    Returns:
        FakeWebsocket: A fake WebSocket client.
    """
    return request.param
