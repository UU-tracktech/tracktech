import asyncio
import os
from src.websocket_client import WebsocketClient
from super_websocket_client import WebsocketClientDummy
import pytest
import tornado
import tornado.testing
import tornado.gen
from tornado import websocket
import tornado.web
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


class TestReceivingFromOrchestrator:
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

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_retrieve_feature_map(self):
        """Sends valid featureMap entry

        """
        ws_client = await self.get_connected_websocket()
        ws_client2 = await self.get_connected_websocket()
        msg = load_data('featureMap', 1)
        await ws_client._write_message(msg[0])
        await asyncio.sleep(1)
        await ws_client2.await_message(1)
        assert len(ws_client2.message_list) == 1
        # ws_client.write_message(json_message[0])

    @pytest.mark.skip
    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_retrieve_start_tracking(self):
        """Sends valid featureMap entry

        """
        ws_client = await self.get_connected_websocket()
        ws_client2 = await self.get_connected_websocket()
        msg = load_data('start', 1)
        await ws_client._write_message(msg[0])
        await asyncio.sleep(1)
        await ws_client2.await_message(1)
        assert len(ws_client2.message_list) == 1
        # ws_client.write_message(json_message[0])

    @pytest.mark.skip
    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_retrieve_stop_tracking(self):
        """Sends valid featureMap entry

        """
        ws_client = await self.get_connected_websocket()
        ws_client2 = await self.get_connected_websocket()
        msg = load_data('stop', 1)
        await ws_client._write_message(msg[0])
        await asyncio.sleep(1)
        await ws_client2.await_message(1)
        assert len(ws_client2.message_list) == 1
        # ws_client.write_message(json_message[0])

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_retrieve_feature_map(self):
        """Sends valid featureMap entry

        """
        ws_client = await self.get_connected_websocket()
        ws_client2 = await self.get_connected_websocket()
        msg = load_data('featureMap', 10)
        for j in msg:
            await ws_client._write_message(j)
        await asyncio.sleep(1)
        await ws_client2.await_message(10)
        assert len(ws_client2.message_list) == 10
        # ws_client.write_message(json_message[0])


if __name__ == '__main__':
    pytest.main(TestReceivingFromOrchestrator)
