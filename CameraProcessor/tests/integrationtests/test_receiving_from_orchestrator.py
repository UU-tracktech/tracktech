import asyncio
from super_websocket_client import WebsocketClientDummy
import pytest
from utils.jsonloader import load_data
from async_timeout import timeout

# Listens to what orchestrator sends through

# Expects to hear messages from orchestrator via other processor
# Gets to hear feature map API calls from orchestrator when other processor sends them

url = 'ws://processor-orchestrator-test-service/processor'
url = 'ws://localhost:80/processor'


def with_timeout(t):
    """Time out function for testing

    Args:
        t: seconds as integer

    Returns: async timer

    """

    def wrapper(corofunc):
        async def run(*args, **kwargs):
            with timeout(t):
                return await corofunc(*args, **kwargs)
        return run
    return wrapper


def __eq__(self, other):
    """Custom equalize function

    Args:
        self: first object to compare
        other: second object to compare

    Returns: bool

    """
    if isinstance(self, other.__class__):
        return self.a == other.a and self.b == other.b
    return False


class TestReceivingFromOrchestrator:

    @staticmethod
    def get_websocket():
        """Sets up WesocketClient superclass for testing

        """
        return WebsocketClientDummy(url)

    async def get_connected_websocket(self):
        """Tests connection to orchestrator

        """
        ws_client = self.get_websocket()
        await ws_client.connect()
        return ws_client

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_confirm_connection(self):
        """Confirms connection with websocket

        """
        ws_client = self.get_websocket()
        await ws_client.connect()
        assert ws_client.connection is not None
        ws_client.connection.close()

    @pytest.fixture(params=['featureMap'])
    def message_type(self, request):
        return request.param

    @pytest.fixture(params=[(1, True), (10, True), (999, False)], ids=["1, True", "10, True", "999, False"])
    def amount(self, request):
        return request.param

    @pytest.mark.asyncio
    async def test_retrieve_data(self, message_type, amount):
        """Sends data to the orchestrator and tests if it receives the same data back

        Args:
            message_type: Pytest fixture, being one of the available message types
            amount: Tuple consisting of any number, or None for all the test data, and a boolean for Random data

        Returns:

        """
        print("GOT HERE 3")
        msg = load_data(message_type, amount[0], amount[1])
        ws_client = await self.get_connected_websocket()
        ws_client2 = await self.get_connected_websocket()
        for j in msg:
            ws_client.write_message(j)
        await ws_client2.await_message(len(msg))
        assert len(ws_client2.message_list) == len(msg)
        for i in msg:
            assert ws_client2.message_list[i.index(i)].__eq__(i)
        ws_client.connection.close()
        ws_client2.connection.close()
        await asyncio.sleep(1)
        task1 = asyncio.create_task(self._check_closed(ws_client))
        task2 = asyncio.create_task(self._check_closed(ws_client2))
        await task1
        await task2

    async def _is_queue_empty(self, ws_client):
        """A coroutine used for waiting until the message queue is empty.

        Args:
            ws_client: the given WebSocketClient
        """
        while(True):
            if not ws_client.write_queue:
                return

    async def _check_closed(self, ws_client):
        while ws_client.connection is not None:
            pass
        return


if __name__ == '__main__':
    pytest.main(TestReceivingFromOrchestrator)
