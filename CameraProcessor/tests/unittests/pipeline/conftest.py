import pytest

from tests.unittests.utils.fake_websocket import FakeWebsocket

"""Can't use fake client because Docker dislikes opencv

"""
# @pytest.fixture(params=[FakeWebsocket(), None], ids=["Fake Client", "None Client"])
# def clients(request):
#     return request.param

@pytest.fixture(params=[None], ids=["No client"])
def clients(request):
    return request.param
