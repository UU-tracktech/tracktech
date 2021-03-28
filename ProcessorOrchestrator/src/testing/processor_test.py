import threading
import pytest
from tornado import websocket
#from src.processor import *
from ..main import *


class TestProcessor:
    @classmethod
    async def setup_class(cls):
        # start server
        threading.Thread(target=main).start()
        cls.socket = await websocket.websocket_connect("ws://localhost")

    def wrong_json_syntax_is_caught_and_logged(self):
        self.socket.write_message("This is not valid json")
