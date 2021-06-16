"""Tests the basic connection functionality: construction, connection and automatic reconnect on connection close.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import asyncio
import pytest

from utils.utils import PC_URL
from processor.webhosting.websocket_client import WebsocketClient


# pylint: disable=attribute-defined-outside-init
class TestConnection:
    """Tests connection."""
    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_websocket_construction(self):
        """Test connecting to websocket."""
        self.ws_client = WebsocketClient(PC_URL, 'mock_id')

        # Connect and test properties.
        await self.ws_client.connect()
        assert self.ws_client.websocket_url == PC_URL
        assert self.ws_client.write_queue == []
        assert not self.ws_client.reconnecting
        assert self.ws_client.connection is not None

        # Disconnect.
        await self.ws_client.disconnect()

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_websocket_disconnecting(self):
        """Test disconnection from websocket."""
        self.ws_client = WebsocketClient(PC_URL, 'mock_id')

        # Assert connection.
        await self.ws_client.connect()
        assert self.ws_client.connection.protocol is not None

        # Assert disconnect.
        await self.ws_client.disconnect()
        assert self.ws_client.connection.protocol is None

    @pytest.mark.asyncio
    @pytest.mark.timeout(10)
    async def test_websocket_reconnect(self):
        """Test connecting, disconnecting and automatic reconnecting."""
        # Global websocket.
        self.ws_client = WebsocketClient(PC_URL, 'mock_id')

        # Assert connection.
        await self.ws_client.connect()
        assert self.ws_client.connection is not None
        self.ws_client.connection.close()

        # Give control back to tornado ioloop.
        await asyncio.sleep(0)
        assert self.ws_client.connection is not None
        await self.ws_client.disconnect()


if __name__ == '__main__':
    pytest.main(TestConnection)
