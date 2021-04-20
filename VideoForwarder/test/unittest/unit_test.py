import pytest
import os
import sys
import json

from src.camera import Camera
from src.camera_handler import CameraHandler
from src.main import convertJsonToCamera


@pytest.fixture
def empty_camera():
    return Camera(None, None)


def create_camera(ip, audio):
    return Camera(ip, audio)


def test_default_initial_conversion(empty_camera):
    assert not empty_camera.conversion


def test_default_initial_callback(empty_camera):
    assert not empty_camera.callback


def test_ip_property():
    ip = "test"
    camera = create_camera(ip, None)
    assert camera.ip_adress == ip


def test_audio_property():
    audio = True
    camera = create_camera(None, audio)
    assert camera.audio


def test_json_conversion():
    json_content = open(os.path.join(os.path.dirname(__file__), 'testConfig.json'))
    json_data = json.load(json_content)
    json_content.close()

    cameras = convertJsonToCamera(json_data)
    camera = cameras["testvid"]
    assert camera.ip_adress == "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
    assert camera.audio
