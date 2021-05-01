"""The request handler that serves the actual HLS index and segment files
It handles authentication/authorization and makes sure conversion processes of cameras are started and stopped

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import os
import re
import threading
import time
from subprocess import TimeoutExpired
import tornado.web
import jwt

from conversion_process import get_conversion_process
from utils import get_stream_variables, get_token_variables


# pylint: disable=attribute-defined-outside-init
class CameraHandler(tornado.web.StaticFileHandler):
    """The camera file request handler

    cameras (dict): Dictionary containing all the cameras registered to this VideoForwarder

    """

    # A dictionary to store all camera objects with their name as key
    cameras = {}

    # pylint: disable=arguments-differ
    def initialize(self, path, default_filename=None):
        """Set the root path and load the public key from application settings, run at the start of every request

        Args:
            path (str): path to root where files are stored
            default_filename (Optional[str] = None): Optional file name
        """
        # Set properties of the handler
        self.remove_delay, self.timeout_delay = get_stream_variables()[3:]

        # noinspection PyAttributeOutsideInit
        # Needed for the library
        super().initialize(path, default_filename)
        self.root = path

        # Load the public key from application settings
        self.public_key = self.application.settings.get('publicKey')

    def set_default_headers(self):
        """Set the headers to allow cors and disable caching
        """
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Cache-control", "no-store")

    def create_stream_conversion(self, camera, abspath, root):
        """Creates stream conversion and starts the stream

        Args:
            camera (str): Name of camera handler that needs to get started
            abspath (str): Path of stream
            root (str): Path to put the
        """
        # Gets camera object
        entry = CameraHandler.cameras[camera]

        # If there is no current conversion, start one
        if entry.conversion is None:
            print(f'starting {camera}')

            # Configure entry conversion
            entry.conversion = get_conversion_process(
                entry.ip_address,
                entry.audio,
                camera,
                root
            )

            # Wait and if not created, stop the conversion
            started = self.stream_started(abspath)
            if not started:
                self.stop_stream(root, camera)

    def stream_started(self, abspath):
        """Wait a maximum of x seconds for the file to be created, otherwise

        Args:
             abspath (path): Path of the file that would be created when stream started
        """
        for _ in range(0, self.timeout_delay):
            # See whether file exists
            if os.path.exists(abspath):
                return True

            # Sleep and check again
            time.sleep(1)

        return False

    @staticmethod
    def stop_stream(root, camera):
        """Function to stop a given camera stream, will be called once a stream is no longer used for a specific
        amount of time

        Args:
            root (str): Root directory of the stream
            camera (Camera): Camera that has to get stopped
        """

        # Print stopping for logging purposes
        print(f'stopping {camera}')

        # Get the camera object that should be stopped
        entry = CameraHandler.cameras[camera]

        # Stopping the conversion
        entry.conversion.terminate()

        try:
            # Wait a few seconds for it stop, so it does not lock any files
            entry.conversion.wait(60)
        except TimeoutExpired:
            # Handle a timeout exception if the process does not stop
            pass
        finally:
            # Remove the conversion
            entry.conversion = None

            # Remove the old segment and index files
            for file in os.listdir(root):
                if file.startswith(camera):
                    os.remove(os.path.join(root, file))

    def start_stream(self, camera, root):
        """Starts the HLS stream by using the conversion process that was created

        Args:
            camera (Camera): Camera to start the stream on
            root (str): Path to the where the stream files are located
        """
        entry = CameraHandler.cameras[camera]

        # Cancel any current callbacks
        if entry.callback is not None:
            entry.callback.cancel()
            entry.callback = None

        # If there is an conversion
        if entry.conversion is not None:
            # Reschedule a new callback to stop the stream
            entry.callback = threading.Timer(
                self.remove_delay, self.stop_stream, [root, camera])
            entry.callback.start()

    def prepare(self):
        """Validate and check the header token if a public key is specified
        """

        # Get variables of tokens
        _, audience, scope = get_token_variables()

        # If a key is specified
        if self.public_key:
            # Decode the token using the given key and the header token
            try:
                decoded = jwt.decode(self.request.headers.get('Authorization').split()[
                                     1], self.public_key, algorithms=['RS256'], audience=audience)
            # If decoding fails, return a 401 not authorized status
            except ValueError as exc:
                self.set_status(401)
                raise tornado.web.Finish() from exc

            # If decoding succeeds, but the scope is invalid, return 403
            if scope in decoded['resource_access'][audience]:
                self.set_status(403)
                raise tornado.web.Finish()

    def get_absolute_path(self, root, path):
        """Gets the path of the camera stream, when the camera is not yet started it does so automatically

        Args:
            root (str): path to the root of the system
            path (str): Name of the file searched, which should be a camera stream

        """

        # Get the path on the file system
        abspath = os.path.abspath(os.path.join(root, path))

        # Regex the file path
        match = re.search(r'(.*?)(?:_V.*)?\.(m3u8|ts)', path)

        # If there is no match, return the path as usual
        if match is None:
            return abspath

        # Otherwise, grab the camera and extension information
        camera = match.group(1)
        extension = match.group(2)

        # If the request is for an index file of an existing camera
        if extension == 'm3u8' and camera in CameraHandler.cameras:
            self.create_stream_conversion(camera, abspath, root)

        # If it requests a stream file
        if extension in ('m3u8', 'ts') and camera in CameraHandler.cameras:
            self.start_stream(camera, root)

        # Return path to files
        return abspath
