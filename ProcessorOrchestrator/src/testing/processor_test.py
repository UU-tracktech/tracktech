import threading
import pytest
from tornado import websocket
from src import main


@pytest.fixture
def app():
    return main.create_app()


async def test_wrong_json_syntax_is_caught_and_logged():
    socket = await websocket.websocket_connect("ws://localhost:80")
    await socket.write_message("This is not valid json")
    assert 1 == 1
