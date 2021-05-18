"""Configurations for the webhosting folders

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import json


def messages_are_equal(str_message, ws_response):
    """Checks whether the messages are equal, for a string message and dictionary format

    Args:
        str_message (str): Message in string format
        ws_response (dict): The response from the websocket is already in dictionary format

    Returns:
        bool: Whether the messages match logically
    """
    expected = json.loads(str_message)
    received = json.loads(str(ws_response).replace("'", '"'))
    return sorted(expected.items()) == sorted(received.items())
