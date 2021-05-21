""" Tests receiving messages from orchestrator, example message pipeline with interface and processor connected

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
# pylint: disable=unused-variable
import asyncio
import json
import pytest
from super_websocket_client import create_dummy_client
from processor.webhosting.start_command import StartCommand
from processor.webhosting.stop_command import StopCommand
from utils.utils import PC_URL, IF_URL


class TestReceivingFromOrchestrator:
    """Class that contains receiving from orchestrator tests
    """
    @pytest.mark.asyncio
    @pytest.mark.timeout(10)
    async def test_confirm_connection(self):
        """Confirms connection with websocket

        """
        ws_client = await create_dummy_client(PC_URL, "mock_id")
        assert ws_client.connection.protocol is not None

    @pytest.fixture(params=['featureMap'])
    def message_type(self, request):
        """Fixture to generate message types

        """
        return request.param

    @pytest.fixture(params=[(1, True), (10, True), (999, False)], ids=["1, True", "10, True", "999, False"])
    def amount(self, request):
        """Fixture to generate message amounts and whether or not invalid messages

        """
        return request.param

    @pytest.mark.asyncio
    async def test_retrieve_start_stop(self):
        """Mock interface client sends a start command to the orchestrator. Check if camera processor handles this
        command properly. Then sends a stop command. Check if camera processor also handles this stop.
        """
        # Get a connected processor client
        processor_client = await create_dummy_client(PC_URL, "mock_id")

        # # Get a connected interface client
        interface_client = await create_dummy_client(IF_URL)

        start_command = json.dumps({"type": "start", "frameId": 1, "boxId": 5, "cameraId": "mock_id"})
        interface_client.write_message(start_command)

        await asyncio.sleep(2)

        received_start = processor_client.message_queue.popleft()
        assert isinstance(received_start, StartCommand)
        assert received_start.box_id == 5
        assert received_start.frame_id == 1

        # Processor orchestrator determines object ID. Should be 1 if this is the first start command.
        assert received_start.object_id == 1

        stop_command = json.dumps({"type": "stop", "objectId": 1})
        interface_client.write_message(stop_command)

        await asyncio.sleep(2)

        received_stop = processor_client.message_queue.popleft()
        assert isinstance(received_stop, StopCommand)
        assert received_stop.object_id == 1

        processor_client.disconnect()
        interface_client.disconnect()

    @staticmethod
    async def _is_queue_empty(ws_client):
        """A coroutine used for waiting until the message queue is empty.

        Args:
            ws_client: the given WebSocketClient
        """
        while True:
            if not ws_client.write_queue:
                return

    @staticmethod
    async def _check_closed(ws_client):
        while ws_client.connection is not None:
            pass
        return


if __name__ == '__main__':
    pytest.main(TestReceivingFromOrchestrator)
