""" Tests the sending of all possibly message types to the processor orchestrator, asserts that nothing is sent back

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import asyncio
import pytest
from super_websocket_client import create_dummy_client
from utils.utils import PC_URL
from utils.jsonloader import load_data


class TestSendToOrchestrator:
    """Class that contains the sending part to orchestrator tests

    """
    @pytest.mark.asyncio
    @pytest.mark.timeout(10)
    async def test_confirm_connection(self):
        """Confirms connection with websocket

        """
        ws_client = await create_dummy_client(PC_URL, "mock_id")
        assert ws_client.connection is not None
        ws_client.connection.close()

    @pytest.mark.asyncio
    async def test_send_message(self, message_type, amount):
        """"Sends a message with different message types
        and in different amounts

        Args:
            message_type: ['boundingBoxes', 'start', 'stop', 'featureMap', 'invalid']
            amount: Tuple consisting of any number, or None for all the test data, and a boolean for Random data
        """
        messages = load_data(message_type, amount[0], amount[1])
        ws_client = await create_dummy_client(PC_URL, "mock_id")
        for msg in messages:
            ws_client.write_message(msg)
        task = asyncio.create_task((self._is_queue_empty(ws_client)))
        await task
        ws_client.connection.close()
        await asyncio.sleep(1)

    @staticmethod
    async def _is_queue_empty(ws_client):
        """A coroutine used for waiting until the message queue is empty.

        Args:
            ws_client: the given WebSocketClient
        """
        while True:
            if not ws_client.write_queue:
                return


if __name__ == '__main__':
    pytest.main(TestSendToOrchestrator())
