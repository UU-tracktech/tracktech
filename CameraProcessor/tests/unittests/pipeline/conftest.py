import pytest

from tests.unittests.utils.fake_websocket import FakeWebsocket

"""Can't use None client because Docker dislikes using windows

"""
# @pytest.fixture(params=[FakeWebsocket(), None], ids=["Fake Client", "None Client"])
# def clients(request):
#     return request.param


@pytest.fixture(params=[FakeWebsocket()], ids=["Fake Client"])
def clients(request):
    return request.param
