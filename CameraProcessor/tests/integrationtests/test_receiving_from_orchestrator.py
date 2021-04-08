""" Tests receiving messages from orchestrator, example message pipeline with interface and processor connected

"""
# pylint: disable=unused-import, unused-variable, unused-argument
import asyncio
import pytest
from super_websocket_client import create_dummy_client
from utils.jsonloader import load_data
from utils.utils import with_timeout, __eq__

# PC_URL= 'ws://processor-orchestrator-test-service/processor'
PC_URL = 'ws://localhost:80/processor'
IF_URL = 'ws://localhost:80/client'


class TestReceivingFromOrchestrator:
    """Class that contains receiving from orchestrator tests

    """
    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_confirm_connection(self):
        """Confirms connection with websocket

        """
        ws_client = await create_dummy_client(PC_URL, "mock_id")
        assert ws_client.connection is not None
        ws_client.connection.close()

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
    @pytest.mark.skip("BUG: PROCESSOR ORCHESTRATOR BUGS ON CONNECTION WITH INTERFACE WEBSOCKET CLIENT?")
    async def test_retrieve_data(self, message_type, amount):
        """Sends data to the orchestrator and tests if it receives the same data back

        Args:
            message_type: Pytest fixture, being one of the available message types
            amount: Tuple consisting of any number, or None for all the test data, and a boolean for Random data

        Returns:

        """
        # Get a connected processor client
        processor_client = await create_dummy_client(PC_URL, "mock_id")

        # Get a connected interface client
        interface_client = await create_dummy_client(IF_URL)

        # msg = load_data(message_type, amount[0], amount[1])
        # ws_client = await self.get_connected_websocket()
        # ws_client2 = await self.get_connected_websocket()
        # for j in msg:
        #     ws_client.write_message(j)
        # await ws_client2.await_message(len(msg))
        # assert len(ws_client2.message_list) == len(msg)
        # for i in msg:
        #     assert ws_client2.message_list[i.index(i)].__eq__(i)
        # ws_client.connection.close()
        # ws_client2.connection.close()
        # await asyncio.sleep(1)
        # task1 = asyncio.create_task(self._check_closed(ws_client))
        # task2 = asyncio.create_task(self._check_closed(ws_client2))
        # await task1
        # await task2

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
