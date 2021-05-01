"""Unit test of the forwarder checks camera.py + json conversion

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
import json

from src.camera import Camera
from src.main import convert_json_to_camera


def create_camera(ip_address, audio):
    """Creates camera with properties in constructor

    Args:
        ip_address: Ip address of a camera
        audio:

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
    ip_address = "test"
    audio = True
    camera = create_camera(ip_address, audio)

    # Asserts properties
    assert camera.ip_address == ip_address
    assert camera.audio


def test_json_conversion():
    """Tests json conversion from testConfig.json

    """
    # Gets json content from file
    json_content = open(os.path.join(os.path.dirname(__file__), 'testConfig.json'))
    json_data = json.load(json_content)
    json_content.close()

    # Create camera from json
    cameras = convert_json_to_camera(json_data)
    camera = cameras["testvid"]

    # Assert properties are set correctly
    assert camera.ip_address == "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
    assert camera.audio
