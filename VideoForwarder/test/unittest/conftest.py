"""Fixture for empty camera

"""
import pytest
from src.camera import Camera


@pytest.fixture
def empty_camera():
    """Creates an empty camera object

    Returns:
        Camera: without ip + audio
    """
    return Camera(None, None)
