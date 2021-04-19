import pytest
import time
import os
import sys
sys.path.insert(1, '/src')

from camera import Camera
from camera_handler import CameraHandler

def create_camera(a,b):
    newCamera = Camera(a,b)
    return newCamera

def test_camera1():
    assert create_camera('1','2').ip == '1'

def test_camera2():
    assert create_camera('1','2').audio == '2'











