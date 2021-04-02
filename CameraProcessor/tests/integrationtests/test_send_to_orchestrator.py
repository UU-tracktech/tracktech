from src.websocket_client import WebsocketClient
import pytest
import os
import json
import tornado
from utils.jsonloader import load_data
from async_timeout import timeout

# Talks to orchestrator

# Sends all possible API calls to orchestrator
# Asserts that no message is sent back to current processor

url = 'ws://processor-orchestrator-test-service/processor'
url = 'ws://localhost:80/processor'


class TestSendToOrchestrator:

    ws_client = WebsocketClient(url)

    async def setup_method(self):

        await self.ws_client.connect()

    def with_timeout(t):
        """Time out function for testing

        Args:
            t: seconds as integer

        Returns: async timer

        """

        def wrapper(corofunc):
            async def run(*args, **kwargs):
                with timeout(t):
                    return await corofunc(*args, **kwargs)

            return run

        return wrapper

    @pytest.mark.asyncio
    @with_timeout(10)
    async def test_confirm_connection(self):
        """Confirms connection with websocket

        """

        assert self.ws_client.connection

    @pytest.mark.parametrize("x", [1, 10])
    def test_send_x_valid_boundingbox_data(self, x):
        """Sends valid boundingbox entry

        """
        m = load_data('boundingBoxes', x)
        self._write_data(m)


    @pytest.mark.parametrize("x", [1, 10])
    def test_send_x_valid_featuremap_data(self, x):
        """Sends valid data entry for bounding boxes

        """
        m = load_data('featureMap', x)
        self._write_data(m)

    @pytest.mark.parametrize("x", [1, 10])
    def test_send_x_invalid_data(self, x):
        """Sends invalid data entry

        """
        m = load_data('invalid', x)
        self._write_data(m)

    @pytest.mark.parametrize("x,y", [(1, 9), (9, 1)])
    def test_send_x_valid_y_invalid(self, x, y):
        """Sends multiple valid data entries and one invalid data entry.

        """
        m = load_data('boundingBoxes', x)
        m.append(load_data('invalid', y))
        self._write_data(m)

    def test_speed_test(self):
        """Speed tests

        """
        pass

    def _write_data(self, message):
        for m in message:
            self.ws_client.write_message(json.dumps(m))


if __name__ == '__main__':
    pytest.main(TestSendToOrchestrator)
