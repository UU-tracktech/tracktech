"""Defines fixtures other integration tests can use for parameterized testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


@pytest.fixture(params=['boundingBoxes', 'featureMap', 'invalid', 'bad'])
def message_type(request):
    """Fixture to generate message types.

    Args:
        request ([object]): Type of messages.
    """
    return request.param


@pytest.fixture(params=[(1, True), (10, True), (999, False)], ids=["1, True", "10, True", "999, False"])
def amount(request):
    """Fixture to generate message amounts and whether invalid messages.

    Args:
        request ([object]): Number of messages and whether the messages should be valid.
    """
    return request.param


@pytest.fixture(params=['full'])
def message_type_receiving(request):
    """"Fixture that sends start, featureMap, and stop.

    Args:
        request ([object]): Fixture parameters given one by one in tests
    """
    return request.param
