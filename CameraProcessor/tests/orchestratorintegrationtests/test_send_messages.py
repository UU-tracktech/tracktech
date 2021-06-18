"""Tests the message sending to the orchestrator.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from utils.utils import PC_URL
from processor.websocket.websocket_client import WebsocketClient
from processor.websocket.boxes_message import BoxesMessage
from processor.websocket.start_message import StartMessage
from processor.websocket.stop_message import StopMessage
from processor.websocket.update_message import UpdateMessage
from processor.data_object.bounding_boxes import BoundingBoxes


class TestSendMessages:
    """Send a single bounding box message."""
    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_send_single_message(self):
        """Test connecting to websocket."""
        ws_client = WebsocketClient(PC_URL, 'mock_id')

        # Connect.
        await ws_client.connect()

        # Send the message.
        ws_client.send_message(BoxesMessage(1., BoundingBoxes([])))

        # Disconnect.
        await ws_client.disconnect()
        assert len(ws_client.write_queue) == 0

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    async def test_invalid_message(self):
        """Tests sending invalid message types. Should be handled orchestrator, so we expect no error."""
        ws_client = WebsocketClient(PC_URL, 'mock_id')

        # Connect.
        await ws_client.connect()

        # Send invalid messages.
        ws_client.send_message(StartMessage(1, box_id=1, frame_id=1.))
        ws_client.send_message(StopMessage(1))
        ws_client.send_message(UpdateMessage(1, [0.]))

        # Disconnect.
        await ws_client.disconnect()
        assert len(ws_client.write_queue) == 0

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_send_many_message(self):
        """Send 1000 bounding box messages as a stress test."""
        ws_client = WebsocketClient(PC_URL, 'mock_id')

        # Connect.
        await ws_client.connect()

        for _ in range(1000):
            ws_client.send_message(BoxesMessage(1., BoundingBoxes([])))

        # Disconnect.
        await ws_client.disconnect()
        assert len(ws_client.write_queue) == 0


if __name__ == '__main__':
    pytest.main(TestSendMessages)
