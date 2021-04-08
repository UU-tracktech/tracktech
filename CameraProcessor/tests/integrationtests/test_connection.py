"""Tests the basic connection functionality: construction, connection and automatic reconnect on connection close.

"""
import asyncio
import pytest
from utils.utils import with_timeout
from src.websocket_client import create_client


# PC_URL = 'ws://processor-orchestrator-test-service/processor'
PC_URL = 'ws://localhost:80/processor' # Processor websocket url


@pytest.mark.asyncio
@with_timeout(10)
async def test_websocket_construction():
    """Test connecting to websocket

    """
    ws_client = await create_client(PC_URL, "mock_id")
    assert ws_client.url == PC_URL
    assert ws_client.write_queue == []
    assert not ws_client.reconnecting
    assert ws_client.connection is not None


@pytest.mark.skip(reason='Possibly unnecessary test; No build in disconnect implemented.')
@pytest.mark.asyncio
@with_timeout(5)
async def test_websocket_disconnecting():
    """Test disconnection from websocket

    """


@pytest.mark.asyncio
@with_timeout(10)
async def test_websocket_reconnect():
    """Test connecting, disconnecting and automatic reconnecting

    """
    # global websocket
    ws_client = await create_client(PC_URL, "mock_id")
    assert ws_client.connection is not None
    ws_client.connection.close()
    await asyncio.sleep(1)
    assert ws_client.connection is not None
