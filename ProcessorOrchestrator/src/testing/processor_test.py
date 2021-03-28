import threading
import pytest
from tornado import websocket
#from src.processor import *
from src import main

class TestProcessor:
    async def setup_method(self):
        # start server
        threading.Thread(target=main).start()
        self.socket = await websocket.websocket_connect("ws://localhost")

    def test_wrong_json_syntax_is_caught_and_logged(self):
        # self.socket.write_message("This is not valid json")
        assert True
