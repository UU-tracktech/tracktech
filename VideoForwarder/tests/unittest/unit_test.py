"""Unit test of the forwarder checks camera.py + json conversion

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
import pytest
import ssl

from src.camera import Camera
from src.main import create_camera, create_stream_options, create_ssl_options,\
    get_remove_delay, get_timeout_delay, create_authenticator
from src.logging_filter import LoggingFilter


def test_camera_properties():
    """Test whether ip_address property has been set correctly

    """
    # Init camera
    url = "test"
    audio = True
    camera = Camera(url, audio)

    # Asserts properties
    assert camera.url == url
    assert camera.audio


def test_camera_environment_1():
    """Test if the camera object gets constructed properly from the environment


    """
    os.environ["CAMERA_URL"] = "camera url"
    os.environ["CAMERA_AUDIO"] = "true"

    camera = create_camera()
    assert camera.url == "camera url"
    assert camera.audio 

    del os.environ['CAMERA_URL']
    del os.environ['CAMERA_AUDIO']


def test_camera_environment_2():
    """Test if an key error is raised when no environment is set

    """

    with pytest.raises(Exception):
        _ = create_camera()


def test_stream_options_1():
    """ Check if the stream properties gets read properly
    """
    os.environ['SEGMENT_SIZE'] = '12'
    os.environ['SEGMENT_AMOUNT'] = '34'
    os.environ['STREAM_ENCODING'] = '56'
    os.environ['STREAM_LOW'] = 'true'
    os.environ['STREAM_MEDIUM'] = 'true'
    os.environ['STREAM_HIGH'] = 'true'

    options = create_stream_options()

    assert options.segment_size == '12'
    assert options.segment_amount == '34'
    assert options.encoding == '56'
    assert options.low
    assert options.medium
    assert options.high

    del os.environ['SEGMENT_SIZE']
    del os.environ['SEGMENT_AMOUNT']
    del os.environ['STREAM_ENCODING']
    del os.environ['STREAM_LOW']
    del os.environ['STREAM_MEDIUM']
    del os.environ['STREAM_HIGH']


def test_stream_options_2():
    """ Check if the default stream options are good
    """

    options = create_stream_options()

    assert options.segment_size == '2'
    assert options.segment_amount == '5'
    assert options.encoding == 'libx264'
    assert not options.low
    assert not options.medium
    assert not options.high


def test_remove_delay_1():
    """ Check if the remove delay gets read properly
    """
    os.environ["REMOVE_DELAY"] = "10"
    delay = get_remove_delay()

    assert delay == 10.0

    del os.environ["REMOVE_DELAY"]


def test_remove_delay_2():
    """ Check if the default remove delay is good
    """
    delay = get_remove_delay()
    assert delay == 60.0


def test_timeout_delay_1():
    """ Check if the timout delay gets read properly
    """
    os.environ["TIMEOUT_DELAY"] = "10"
    delay = get_timeout_delay()

    assert delay == 10.0

    del os.environ["TIMEOUT_DELAY"]


def test_timeout_delay_2():
    """ Check if the default timout delay is good
    """
    delay = get_timeout_delay()
    assert delay == 30.0


def test_ssl_1():
    """ Check if the ssl context is not None if proper certificates are supplied
    """
    os.environ['SSL_CERT'] = '/app/tests/files/cert.pem'
    os.environ['SSL_KEY'] = '/app/tests/files/key.pem'

    try:
        assert create_ssl_options() is not None
    finally:
        del os.environ['SSL_CERT']
        del os.environ['SSL_KEY']


def test_ssl_2():
    """ Check if the ssl context is None if not both environment variables are supplied
    """
    assert create_ssl_options() is None


def test_ssl_3():
    """ Check if the ssl context fails if given wrong paths
    """
    os.environ['SSL_CERT'] = 'path 1'
    os.environ['SSL_KEY'] = 'path 2'

    with pytest.raises(FileNotFoundError):
        _ = create_ssl_options()

    del os.environ['SSL_CERT']
    del os.environ['SSL_KEY']


def test_ssl_4():
    """ Check if the ssl context fails if wrong files are supplied
    """
    os.environ['SSL_CERT'] = '/app/tests/files/key.pem'
    os.environ['SSL_KEY'] = '/app/tests/files/key.pem'

    with pytest.raises(ssl.SSLError):
        _ = create_ssl_options()

    del os.environ['SSL_CERT']
    del os.environ['SSL_KEY']


def test_authenticator_1():
    """ Check if the authenticator is not None if all properties are specified
    """
    os.environ["PUBLIC_KEY"] = "/app/tests/files/key.pem"
    os.environ["AUDIENCE"] = "aud"
    os.environ["CLIENT_ROLE"] = "role"

    authenticator = create_authenticator()

    # assert authenticator.public_key ==
    assert authenticator.audience == "aud"
    assert authenticator.role == "role"

    del os.environ["PUBLIC_KEY"]
    del os.environ["AUDIENCE"]
    del os.environ["CLIENT_ROLE"]


def test_authenticator_2():
    """ Check if the authenticator is None if not all properties are specified
    """
    assert create_authenticator() is None


def test_filter_1():
    """ Check if normal requests are logged
    """
    assert LoggingFilter().filter(LogRecord('name', 0, 'path', 0, '%s %s', ('key', 'value'), None))


def test_filter_2():
    """ Check if 200 get requests are not logged
    """
    assert not LoggingFilter().filter(LogRecord('name', 0, 'path', 0, '200 GET %s %s', ('key', 'value'), None)) 