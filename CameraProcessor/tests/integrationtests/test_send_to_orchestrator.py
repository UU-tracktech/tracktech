import asyncio
from src.websocket_client import WebsocketClient
import pytest
import tornado
import tornado.testing
import tornado.gen
from tornado import websocket
import tornado.web
import jsonloader
from async_timeout import timeout

# Talks to orchestrator

# Sends all possible API calls to orchestrator
# Asserts that no message is sent back to current processor

url = 'ws://processor-orchestrator-test-service/processor'
url = 'ws://localhost:80/processor'


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


websocket_test = WebsocketClient(url)


async def test_confirm_connection():
    """Confirms connection with websocket

    """
    assert websocket_test.connection


def test_send_single_valid_data():
    """Sends single valid data entry

    """
    pass


def test_send_single_invalid_data():
    """Sends single invalid data entry

    """
    pass


def test_send_10_valid_data():
    """Sends multiple valid data entries

    """
    pass


def test_send_9_valid_1_invalid():
    """Sends multiple valid data entries and one invalid data entry.

    """
    pass


def test_speed_test():
    """Speed tests

    """
    pass
