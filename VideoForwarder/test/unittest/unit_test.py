import pytest
import os
import sys
import json

sys.path.insert(1, '/src')
from camera import Camera
from camera_handler import CameraHandler
from main import convertJsonToCamera


@pytest.fixture
def empty_camera():
    return Camera(None, None)

def create_camera(ip, audio):
    return Camera(ip, audio)

def test_default_initial_conversion(empty_camera):
    assert empty_camera.conversion == None

def test_default_initial_callback(empty_camera):
    assert empty_camera.callback == None

def test_ip_property():
    ip = "test"
    camera = create_camera(ip, None)
    assert camera.ip == ip

def test_audio_property():
    audio = True
    camera = create_camera(None, audio)
    assert camera.audio == True

def test_json_conversion():
    json_file = open('testConfig.json', )
    json_data = json.load(json_file)
    json_file.close()

    cameras = convertJsonToCamera(json_data)
    camera = cameras["testvid"]
    assert camera.ip == "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov" and camera.audio
