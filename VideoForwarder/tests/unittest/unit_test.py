"""Unit test of the forwarder checks camera.py + json conversion

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
import json

from src.camera import Camera


def create_camera(ip_address, audio):
    """Creates camera with properties in constructor

    Args:
        ip_address (str): Ip address of a camera
        audio (bool): Whether camera contains audio

    Returns:
        Create a camera with properties
    """
    return Camera(ip_address, audio)


def test_default_properties(empty_camera):
    """Tests default properties of an empty camera object

    Args:
        empty_camera (Camera): Empty camera

    """
    assert not empty_camera.conversion
    assert not empty_camera.callback


def test_camera_properties():
    """Test whether ip_address property has been set correctly

    """
    # Init camera
    url = "test"
    audio = True
    camera = create_camera(url, audio)

    # Asserts properties
    assert camera.url == url
    assert camera.audio
    