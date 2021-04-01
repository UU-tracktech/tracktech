import asyncio
from src.websocket_client import WebsocketClient
import pytest
import tornado
import tornado.testing
import tornado.gen
from tornado import websocket
import tornado.web
import jsonloader
from async_timeout import timeout

# Make with_timeout available from everywhere (as fixture?)\
# Constructor
# Connects
# Disconnects
# Reconnect
# Test API call

url = 'ws://processor-orchestrator-test-service/processor'
url = 'ws://localhost:80/processor'


def with_timeout(t):
    def wrapper(corofunc):
        async def run(*args, **kwargs):
            with timeout(t):
                return await corofunc(*args, **kwargs)
        return run
    return wrapper


def test_websocket_constructor():
    # global websocket
    websocket_test = WebsocketClient(url)
    assert websocket_test.url == url
    assert websocket_test.write_queue == []
    assert not websocket_test.reconnecting
    assert not websocket_test.connection
    assert not websocket_test.connected


@pytest.mark.asyncio
@with_timeout(10)
async def test_connecting():
    # global websocket
    websocket_test = WebsocketClient(url)
    await websocket_test.connect()
    assert websocket_test.connection


@pytest.mark.asyncio
@with_timeout(5)
async def test_websocket_disconnecting():
    # global websocket
    websocket_test = WebsocketClient(url)
    await websocket_test.connect()
    # assert pytest.raises(AttributeError, PreAnnotations, example_text_file, nr_frames)
    assert websocket_test.connection is not None
    await websocket.gen.sleep(1)
    websocket_test.on_close()
    await websocket.gen.sleep(1)
    assert not websocket_test.connected


@pytest.mark.asyncio
@with_timeout(10)
async def test_websocket_reconnect():
    # global websocket
    websocket_test = WebsocketClient(url)
    await websocket_test.connect()
    assert websocket_test.connection
    websocket_test.connection.close()
    await websocket_test.connect()
    assert websocket_test.connection
