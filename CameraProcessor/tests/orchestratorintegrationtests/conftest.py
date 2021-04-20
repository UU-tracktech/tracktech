import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


@pytest.fixture(params=['boundingBoxes', 'start', 'stop', 'featureMap', 'invalid', 'bad'])
def message_type(request):
    """Fixture to generate message types

    """
    return request.param


@pytest.fixture(params=[(1, True), (10, True), (999, False)], ids=["1, True", "10, True", "999, False"])
def amount(request):
    """Fixture to generate message amounts and whether or not invalid messages

    """
    return request.param

@pytest.fixture(params=['full'])
def message_type_receiving(request):
    """"Fixture that sends start, featureMap, and stop"

    """
    return request.param
