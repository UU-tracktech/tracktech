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
    websocket = WebsocketClient(url)
    assert websocket.url == url
    assert websocket.write_queue == []
    assert not websocket.reconnecting
    assert not websocket.connection


@pytest.mark.asyncio
@with_timeout(10)
async def test_connecting():
    # global websocket
    websocket = WebsocketClient(url)
    await websocket.connect()
    assert websocket.connection


@pytest.mark.asyncio
@with_timeout(2)
async def test_websocket_disconnecting():
    # global websocket
    websocket = WebsocketClient(url)
    await websocket.connect()
    # assert pytest.raises(AttributeError, PreAnnotations, example_text_file, nr_frames)
    websocket.on_close()
    await asyncio.sleep(1)
    assert websocket.start_tracking("test")


@pytest.mark.asyncio
@with_timeout(10)
async def test_websocket_reconnect():
    # global websocket
    websocket = WebsocketClient(url)
    await websocket.connect()
    assert websocket.connection
    websocket.connection.close()
    await websocket.connect()
    assert websocket.connection
