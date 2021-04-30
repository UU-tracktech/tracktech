"""Mock websocket for testing.

"""
import json


class FakeWebsocket:
    """A fake websocket that implements the same methods but just asserts the

    """

    def write_message(self, message):
        """Takes a message and asserts if it has the correct type property

        Args:
            message: a JSON object

        """
        msg = json.loads(message)
        assert msg["type"] == 'boundingBoxes'
