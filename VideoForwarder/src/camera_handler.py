"""The request handler that serves the actual HLS index and segment files.

It handles authentication/authorization and makes sure conversion processes of cameras are started and stopped

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import os
import re
import threading
import time
from logging import info, error
from subprocess import TimeoutExpired
from tornado.web import StaticFileHandler
import tornado
from auth.auth import AuthenticationError, AuthorizationError

from src.conversion_process import get_conversion_process


# pylint: disable=attribute-defined-outside-init
class CameraHandler(StaticFileHandler):
    """The camera file request handler.

    Attributes:
        remove_delay (float): After how much time the section files will be removed from memory.
        timeout_delay (int): After how much time the client becomes inactive.
        wait_delay (int): Time it waits before stopping the stream.
        stream_options (StreamOptions): Contains all the options of the stream.
        authenticator (Auth): Authentication object of the handler.
        camera (Camera): Camera that is being served.
    """

    def initialize(self, path, default_filename=None):
        """Set the root path and load the public key from application settings, run at the start of every request.

        Args:
            path (str): path to root where files are stored.
            default_filename (Optional[str] = None): Optional file name.
        """
        super().initialize(path, default_filename)

        # Set properties of the handler.
        self.remove_delay = self.application.settings.get("remove_delay")
        self.timeout_delay = self.application.settings.get("timeout_delay")
        self.wait_delay = self.application.settings.get("wait_delay")

        self.stream_options = self.application.settings.get("stream_options")

        # Load the public key from application settings.
        self.authenticator = self.application.settings.get("authenticator")

        # Load the camera object from application settings.
        self.camera = self.application.settings.get("camera")

    def set_default_headers(self):
        """Set the headers to allow cors and disable caching."""
        self.set_header("Cache-control", "no-store")
        self.set_header("Access-Control-Allow-Origin", "*")

        # Allow Authorization header to keep cors preflight happy.
        self.set_header('Access-Control-Allow-Headers', 'Authorization')

    def options(self, _path_args, **_path_kwargs):
        """Handle an options request and set response to "no content success".

        Args:
            _path_args (Any): Arguments given to the path.
            **_path_kwargs (Any): Any other arguments given to the method.
        """
        self.set_status(204)
        self.finish()

    def start_stream(self, root):
        """Creates stream conversion and starts the stream.

        Args:
            root (str): Path to the streams folder.
        """

        # If there is no current conversion, start one.
        if self.camera.conversion is None:
            info("starting stream")

            # Configure entry conversion.
            self.camera.conversion = get_conversion_process(
                self.camera.url,
                self.camera.audio,
                root,
                self.stream_options
            )

            # Wait and if not created, stop the conversion.
            started = self.stream_active(root)
            if not started:
                self.stop_stream(root)

    def stream_active(self, root):
        """Wait a maximum of x seconds for the file to be created, otherwise.

        Args:
             root (path): path of the folder that contains the stream segments and index files.
        """

        index_file_path = os.path.join(root, "stream.m3u8")

        for _ in range(0, self.timeout_delay):

            # See whether file exists.
            if os.path.exists(index_file_path):
                return True

            # Sleep and check again.
            time.sleep(1)

        return False

    def restart_stop_callback(self, root):
        """Starts the HLS stream by using the conversion process that was created.

        Args:
            root (str): Path to the where the stream files are located.
        """

        # Cancel any current callbacks.
        if self.camera.callback is not None:
            self.camera.callback.cancel()
            self.camera.callback = None

        # If there is an conversion.
        if self.camera.conversion is not None:
            # Reschedule a new callback to stop the stream.
            self.camera.callback = threading.Timer(
                self.remove_delay, self.stop_stream, [root])
            self.camera.callback.start()

    def stop_stream(self, root):
        """Called once a stream is no longer used for a specific amount of time.

        Args:
            root (str): Root directory of the stream.
        """

        # Print stopping for logging purposes.
        info("stopping stream")

        # Stopping the conversion.
        self.camera.conversion.terminate()

        try:
            # Wait a few seconds for it stop, so it does not lock any files.
            self.camera.conversion.wait(self.wait_delay)
        except TimeoutExpired:
            # Handle a timeout exception if the process does not stop.
            pass
        finally:
            # Remove the conversion.
            self.camera.conversion = None

            # Remove the old segment and index files.
            for file in os.listdir(root):
                os.remove(os.path.join(root, file))

    # pylint: disable=broad-except
    def prepare(self):
        """Validate and check the header token if a public key is specified."""

        # Validate the token and act accordingly if it is not good.
        if self.authenticator is not None and self.request.method != 'OPTIONS':
            try:
                header = self.request.headers.get('Authorization')
                if header is not None:
                    method, content = header.split()
                    if method == 'Bearer':
                        self.authenticator.validate(content)
                    else:
                        raise AuthenticationError('Unimplemented authorization method')
                else:
                    # Url parameter bc video.js does not want to send headers with the index file request.
                    self.authenticator.validate(self.get_argument('Bearer'))

            except AuthenticationError as exc:
                # Authentication (validating token) failed.
                error(exc)
                self.set_status(403)
                raise tornado.web.Finish() from exc
            except AuthorizationError as exc:
                # Authorization failed (authentication succeeded, but the action is not allowed).
                error(exc)
                self.set_status(401)
                raise tornado.web.Finish() from exc
            except Exception as exc:
                # Any other error, no token added e.g.
                error(exc)
                self.set_status(403)
                raise tornado.web.Finish() from exc

    def get_absolute_path(self, root, path):
        """Gets the path of the camera stream, when the camera is not yet started it does so automatically.

        Args:
            root (str): path to the root of the system.
            path (str): Name of the file searched, which should be a camera stream.

        Returns:
            Path: The absolute path to the stream files.
        """

        # Get the path on the file system.
        abspath = os.path.abspath(os.path.join(root, path))

        # Regex the file path.
        match = re.search(r'stream(?:_V.*)?\.(m3u8|ts)', path)

        # If there is no match, return the path as usual.
        if match is None:
            return abspath

        # Otherwise, grab the camera and extension information.
        extension = match.group(1)

        # If the request is for an index file of an existing camera.
        if extension == 'm3u8':
            self.start_stream(root)

        self.restart_stop_callback(root)

        # Return path to files.
        return abspath
