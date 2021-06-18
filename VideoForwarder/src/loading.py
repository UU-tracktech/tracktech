"""Helper methods to load settings.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import ssl
from os import environ
from logging import info

from auth.auth import Auth
from src.camera import Camera
from src.stream_options import StreamOptions


def create_camera():
    """Creat the camera using the URL and whether the camera has audio.

    Returns:
        Camera: A camera object containing the camera url and if it has any audio.
    """
    return Camera(environ['CAMERA_URL'], environ['CAMERA_AUDIO'] == 'true')


def create_stream_options():
    """Create the stream options for the camera.

    Returns:
        StreamOptions: Load the stream options used for the conversion.
    """
    return StreamOptions(
        environ.get('SEGMENT_SIZE') or '2',
        environ.get('SEGMENT_AMOUNT') or '5',
        environ.get('STREAM_ENCODING') or 'libx264',
        environ.get('STREAM_LOW') == 'true',
        environ.get('STREAM_MEDIUM') == 'true',
        environ.get('STREAM_HIGH') == 'true'
    )


def get_remove_delay():
    """Get the delay after which conversion process is stopped.

    Returns:
        float: How long the stream has no requests before stopping the conversion in seconds.
    """
    return float(environ.get('REMOVE_DELAY') or '60.0')


def get_timeout_delay():
    """Get the delay before the stream will become inactive.

    Returns:
        int: Maximum amount of seconds that will be waited before removing stream files after stopping the conversion.
    """
    return int(environ.get('TIMEOUT_DELAY') or '30')


def get_wait_delay():
    """Get the delay to wait for from the environment.

    Returns:
        int: Waiting time between timeout and deleting files.
    """
    return int(environ.get('WAIT_DELAY') or '60')


def create_ssl_options():
    """Create the context with the given ssl options.

    Returns:
        ssl.SSLContext: an ssl_context to be used by the application.
    """

    # Load environment variable path of certificate and its key.
    cert = environ.get('SSL_CERT')
    key = environ.get('SSL_KEY')

    # If one if missing, return None and do not use ssl.
    if cert is None or key is None:
        return None

    # Create the ssl context.
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(cert, key)

    return ssl_ctx


def create_authenticator():
    """Creates the authenticator for the stream.

    Returns:
        Auth: Auth object containing used to validate tokens.
    """
    # Get variables from the environment.
    public_key, audience, client_role =\
        environ.get('PUBLIC_KEY'), environ.get('AUDIENCE'), environ.get('CLIENT_ROLE')

    # Environment variables not set, so return empty.
    if public_key is None or audience is None or client_role is None:
        return None

    # Give back the Authentication object.
    info('using client token validation.')
    return Auth(
        public_key_path=public_key,
        algorithms=['RS256'],
        audience=audience,
        role=client_role
    )
