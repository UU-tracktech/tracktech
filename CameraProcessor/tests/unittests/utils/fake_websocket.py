"""Mock websocket for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

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
