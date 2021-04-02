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

# url = 'ws://processor-orchestrator-test-service/processor'
url = 'ws://localhost:80/processor'


class TestReceivingFromOrchestrator:

    def setup_method(self):
        self.ws_client = WebsocketClient(url)

    def with_timeout(t):
        def wrapper(corofunc):
            async def run(*args, **kwargs):
                with timeout(t):
                    return await corofunc(*args, **kwargs)

            return run

        return wrapper


websocket_test = WebsocketClient(url)

if __name__ == '__main__':
    pytest.main(TestReceivingFromOrchestrator)
