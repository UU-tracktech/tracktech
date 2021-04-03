from src.websocket_client import WebsocketClient
import pytest
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
        return WebsocketClient(url)

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

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_send_1_valid_boundingbox_data(self):
        """Sends valid boundingbox entry

        """
        ws_client = await self.get_connected_websocket()
        json_message = load_data('boundingBoxes', 1)
        ws_client.write_message(json_message[0])

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_send_10_valid_boundingbox_data(self):
        """Sends valid boundingbox entry

        """
        ws_client = await self.get_connected_websocket()
        json_message = load_data('boundingBoxes', 10)
        for i in json_message:
            ws_client.write_message(i)

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_send_1_valid_featuremap_data(self):
        """Sends valid data entry for bounding boxes

        """
        ws_client = await self.get_connected_websocket()
        json_message = load_data('featureMap', 1)
        ws_client.write_message(json_message[0])

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_send_10_valid_featuremap_data(self):
        """Sends valid data entry for bounding boxes

        """
        ws_client = await self.get_connected_websocket()
        json_message = load_data('featureMap', 10)
        for i in json_message:
            ws_client.write_message(i)

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_send_1_invalid_data(self):
        """Sends invalid data entry

        """
        ws_client = await self.get_connected_websocket()
        json_message = load_data('invalid', 1)
        ws_client.write_message(json_message[0])

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_send_10_invalid_data(self):
        """Sends invalid data entry

        """
        ws_client = await self.get_connected_websocket()
        json_message = load_data('invalid', 10)
        for i in json_message:
            ws_client.write_message(i)

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_send_1_valid_9_invalid(self):
        """Sends multiple invalid data entries and one valid data entry.

        """
        ws_client = await self.get_connected_websocket()
        json_message = load_data('invalid', 9)
        json_message.append(load_data('boundingBoxes', 1)[0])
        for i in json_message:
            ws_client.write_message(i)

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_send_9_valid_1_invalid(self):
        """Sends multiple valid data entries and one invalid data entry.

        """
        ws_client = await self.get_connected_websocket()
        json_message = load_data('boundingBoxes', 9)
        json_message.append(load_data('invalid', 1)[0])
        for i in json_message:
            ws_client.write_message(i)


if __name__ == '__main__':
    pytest.main(TestSendToOrchestrator())
