import pytest
import json
import logging


class FakeWebsocket:
    """A fake websocket that implements the same methods but just asserts the

    """

    def write_message(self, message):
        msg = json.loads(message)
        assert msg["type"] == 'boundingBoxes'