import asyncio
import os
from src.websocket_client import WebsocketClient
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
        return WebsocketClient(url)

    async def get_connected_websocket(self):
        ws_client = self.get_websocket()
        await ws_client.connect()
        return ws_client

    @with_timeout(120)
    async def on_message(self):
        ws_client = self.get_websocket()
        await ws_client.connect()
        m = None
        while m is None:
            m = ws_client.update_feature_map()


    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_confirm_connection(self):
        """Confirms connection with websocket

        """
        ws_client = self.get_websocket()
        await ws_client.connect()
        assert ws_client.connected

    @pytest.mark.asyncio
    @with_timeout(120)
    async def retrieve_feature_map(self):
        """Sends valid boundingbox entry

        """
        ws_client = await self.get_connected_websocket()
        ws_client2 = await self.get_connected_websocket()
        ws_client.write_message(load_data('featureMap', 1))
        await ws_client2.on_message()
        await tornado.gen.sleep(10)
        # ws_client.write_message(json_message[0])


if __name__ == '__main__':
    pytest.main(TestReceivingFromOrchestrator)
