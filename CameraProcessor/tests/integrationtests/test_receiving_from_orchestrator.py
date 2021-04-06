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
        assert ws_client.connected
        ws_client.connection.close()

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_retrieve_feature_map(self):
        """Sends valid featureMap entry and verifies the result

        """
        ws_client = await self.get_connected_websocket()
        ws_client2 = await self.get_connected_websocket()
        msg = load_data('featureMap', 1)
        ws_client.write_message(msg[0])
        await asyncio.sleep(1)
        await ws_client2.await_message(1)
        assert len(ws_client2.message_list) == 1
        assert ws_client2.message_list.__eq__(msg)

    @pytest.mark.skip(reason="Skipping due to no return implementation from orchestrator")
    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_retrieve_start_tracking(self):
        """Sends valid start entry and verifies the result

        """
        ws_client = await self.get_connected_websocket()
        ws_client2 = await self.get_connected_websocket()
        msg = load_data('start', 1)
        ws_client.write_message(msg[0])
        await asyncio.sleep(1)
        await ws_client2.await_message(1)
        assert len(ws_client2.message_list) == 1
        assert ws_client2.message_list.__eq__(msg)
        # ws_client.write_message(json_message[0])

    @pytest.mark.skip(reason="Skipping due to no return implementation from orchestrator")
    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_retrieve_stop_tracking(self):
        """Sends valid stop entry and verifies the result

        """
        ws_client = await self.get_connected_websocket()
        ws_client2 = await self.get_connected_websocket()
        msg = load_data('stop', 1)
        ws_client.write_message(msg[0])
        await asyncio.sleep(1)
        await ws_client2.await_message(1)
        assert len(ws_client2.message_list) == 1
        assert ws_client2.message_list.__eq__(msg)

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_retrieve_feature_map(self):
        """Sends valid featureMap entries and verifies the result

        """
        ws_client = await self.get_connected_websocket()
        ws_client2 = await self.get_connected_websocket()
        msg = load_data('featureMap', 10)
        for j in msg:
            ws_client.write_message(j)
        await asyncio.sleep(1)
        await ws_client2.await_message(10)
        assert len(ws_client2.message_list) == 10
        for i in msg:
            assert ws_client2.message_list[i.index(i)].__eq__(i)

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_retrieve_invalid_tracking(self):
        """Sends valid stop entry and verifies the result

        """
        ws_client = await self.get_connected_websocket()
        ws_client2 = await self.get_connected_websocket()
        msg = load_data('invalid', 1)
        ws_client.write_message(msg[0])
        await asyncio.sleep(1)
        await ws_client2.await_message(1)
        assert len(ws_client2.message_list) == 1
        assert ws_client2.message_list.__eq__(msg)


if __name__ == '__main__':
    pytest.main(TestReceivingFromOrchestrator)
