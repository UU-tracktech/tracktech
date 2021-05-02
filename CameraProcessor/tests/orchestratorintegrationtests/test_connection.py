"""Tests the basic connection functionality: construction, connection and automatic reconnect on connection close.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import asyncio
import pytest
from utils.utils import PC_URL
from processor.websocket_client import create_client


class TestConnection:
    """Tests connection."""

    @pytest.mark.asyncio
    @pytest.mark.timeout(10)
    async def test_websocket_construction(self):
        """Test connecting to websocket

        """
        ws_client = await create_client(PC_URL, "mock_id")
        assert ws_client.url == PC_URL
        assert ws_client.write_queue == []
        assert not ws_client.reconnecting
        assert ws_client.connection is not None

    @pytest.mark.skip(reason='Possibly unnecessary test; No build in disconnect implemented.')
    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_websocket_disconnecting(self):
        """Test disconnection from websocket

        """

    @pytest.mark.asyncio
    @pytest.mark.timeout(10)
    async def test_websocket_reconnect(self):
        """Test connecting, disconnecting and automatic reconnecting

        """
        # global websocket
        ws_client = await create_client(PC_URL, "mock_id")
        assert ws_client.connection is not None
        ws_client.connection.close()
        await asyncio.sleep(1)
        assert ws_client.connection is not None


if __name__ == '__main__':
    pytest.main(TestConnection)
