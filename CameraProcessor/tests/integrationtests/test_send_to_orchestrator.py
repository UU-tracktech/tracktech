from src.websocket_client import WebsocketClient
from super_websocket_client import WebsocketClientDummy
import pytest
import asyncio
from utils.jsonloader import load_data
from async_timeout import timeout

# Talks to orchestrator

# Sends all possible API calls to orchestrator
# Asserts that no message is sent back to current processor

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


class TestSendToOrchestrator:
    @staticmethod
    def get_websocket():
        return WebsocketClientDummy(url)

    async def get_connected_websocket(self):
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
        assert ws_client.connected
        ws_client.connection.close()

    @pytest.fixture(params=['boundingBoxes', 'start', 'stop', 'featureMap', 'invalid', 'bad'])
    def message_type(self, request):
        return request.param

    @pytest.fixture(params=[(1, True), (10, True), (999, False)], ids=["1, True", "10, True", "999, False"])
    def amount(self, request):
        return request.param

    @pytest.mark.asyncio
    async def test_send_message(self, message_type, amount):
        """"Sends a message with different message types
        and in different amounts

        Args:
            message_type: ['boundingBoxes', 'start', 'stop', 'featureMap', 'invalid']
            amount: Tuple consisting of any number, or None for all the test data, and a boolean for Random data
        """
        message = load_data(message_type, amount[0], amount[1])
        ws_client = await self.get_connected_websocket()
        for m in message:
            ws_client.write_message(m)
        task = asyncio.create_task((self._is_queue_empty(ws_client)))
        await task
        ws_client.connection.close()
        await asyncio.sleep(1)

    async def _is_queue_empty(self, ws_client):
        """A coroutine used for waiting until the message queue is empty.

        Args:
            ws_client: the given WebSocketClient
        """
        while(True):
            if not ws_client.write_queue:
                return


if __name__ == '__main__':
    pytest.main(TestSendToOrchestrator())
