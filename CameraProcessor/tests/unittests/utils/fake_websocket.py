"""Mock websocket for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from collections import deque


class FakeWebsocket:
    """A fake websocket that implements the same methods but just mocks some functionality.

    Attributes:
        message_queue (deque): deque object the messages get saved in.
    """
    def __init__(self):
        """Create a message queue in order to save the messages."""
        self.message_queue = deque()

    def send_message(self, message):
        """Sends mock message.

        Args:
            message (IMessage): message to "send".

        Returns:
            (IMessage): The message itself.
        """
        return message
