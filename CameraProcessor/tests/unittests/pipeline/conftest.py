import pytest

from tests.unittests.utils.fake_websocket import FakeWebsocket


@pytest.fixture(params=[FakeWebsocket(), None], ids=["Fake Client", "None Client"])
def clients(request):
    return request.param
