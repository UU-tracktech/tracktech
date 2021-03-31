from src.websocket_client import WebsocketClient
import pytest
import jsonloader
from async_timeout import timeout

url = 'ws://processor-orchestrator-test-service/processor'
url = 'ws://localhost:80/processor'
websocket = None


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
@with_timeout(5)
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
    assert websocket.connection
    websocket.connection.close()
    assert not websocket.connection


@pytest.mark.asyncio
@with_timeout(10)
async def test_websocket_reconnect():
    # global websocket
    websocket = WebsocketClient(url)
    websocket.connect
    assert websocket.connection
    websocket.connection.close()
    await websocket.connect()
    assert websocket.connection