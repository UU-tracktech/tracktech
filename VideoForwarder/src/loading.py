import ssl
import os
import tornado.web

from auth.auth import Auth
from src.camera import Camera
from src.stream_options import StreamOptions


def create_camera():
    """
    Returns:
        A camera object containing the camera url and if it has any audio
    """
    return Camera(os.environ["CAMERA_URL"], os.environ["CAMERA_AUDIO"] == "true")


def create_stream_options():
    """

    Returns:
        StreamOptions: Load the stream options used for the conversion

    """
    return StreamOptions(
        os.environ.get("SEGMENT_SIZE") or "2",
        os.environ.get("SEGMENT_AMOUNT") or "5",
        os.environ.get("STREAM_ENCODING") or "libx264",
        os.environ.get("STREAM_LOW") == "true",
        os.environ.get("STREAM_MEDIUM") == "true",
        os.environ.get("STREAM_HIGH") == "true"
    )


def get_remove_delay():
    """
    Returns:
        float: How long the stream has no requests before stopping the conversion in seconds
    """
    return float(os.environ.get('REMOVE_DELAY') or '60.0')


def get_timeout_delay():
    """
    Returns:
        int: The maximum amount of seconds we will wait with removing stream files after stopping the conversion
    """
    return int(os.environ.get('TIMEOUT_DELAY') or '30')


def get_wait_delay():
    """
    Returns:
        int: How long we will wait for the conversion process to stop before deleting the files
    """
    return int(os.environ.get('REMOVE_DELAY') or '60')


def create_ssl_options():
    """
    Returns:
        ssl.SSLContext: an ssl_context to be used by the application
    """

    # Load environment variable path of certificate and its key
    cert = os.environ.get('SSL_CERT')
    key = os.environ.get('SSL_KEY')

    # If one if missing, return None and do not use ssl
    if cert is None or key is None:
        return None

    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(cert, key)

    return ssl_ctx


def create_authenticator():
    """
    Returns:
        Auth: Auth object containing used to validate tokens
    """
    #
    public_key, audience, client_role =\
        os.environ.get('PUBLIC_KEY'), os.environ.get('AUDIENCE'), os.environ.get('CLIENT_ROLE')
    if public_key is None or audience is None or client_role is None:
        return None
    tornado.log.gen_log.info("using client token validation")
    return Auth(
        public_key_path=public_key,
        algorithms=['RS256'],
        audience=audience,
        role=client_role
    )

