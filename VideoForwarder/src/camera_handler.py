"""
The request handler that serves the actual HLS index and segment files
It handles authentication/authorization and makes sure conversion processes of cameras are started and stopped
"""

import os
import re
import threading
import time
from subprocess import Popen, TimeoutExpired
import tornado.web
import jwt


class CameraHandler(tornado.web.StaticFileHandler):
    """
    The camera file request handler
    """
    def __init__(self):
        """Create attributes

        """
        self.root = None
        self.public_key = None

    cameras = {}
    """A dictionary to store all camera objects with their name as key"""

    segmentSize = os.environ.get('SEGMENT_SIZE') or '1'
    """How long each video segment should be in seconds"""

    segmentAmount = os.environ.get('SEGMENT_AMOUNT') or '5'
    """How many segments of a video stream should be stored at once at a given time"""

    removeDelay = float(os.environ.get('REMOVE_DELAY') or '60.0')
    """How long the stream has no requests before stopping the conversion in seconds"""

    timeoutDelay = int(os.environ.get('TIMEOUT_DELAY') or '30')
    """The maximum amount of seconds we will wait with removing stream files after stopping the conversion"""

    encoding = os.environ['ENCODING']
    """The FFMPEG encoding that should be used to encode the video streams"""

    secret = os.environ.get('JWT_PUBLIC_SECRET')
    """The public secret of the identity provider to validate the tokens with"""

    audience = os.environ.get('TOKEN_AUDIENCE')
    """The audience the token should be for"""

    scope = os.environ.get('TOKEN_SCOPE')
    """The scope the token should be for"""

    # pylint: disable=arguments-differ
    def initialize(self, path):
        """Set the root path and load the public key from application settings, run at the start of every request"""

        # noinspection PyAttributeOutsideInit
        # Needed for the library
        self.root = path

        # Load the public key from application settings
        self.public_key = self.application.settings.get('publicKey')

    def set_default_headers(self):
        """Set the headers to allow cors and disable caching"""

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Cache-control", "no-store")

    @staticmethod
    def stop_stream(root, camera):
        """Function to stop a given camera stream, will be called once a stream is no longer used for a specific
        amount of time """

        # Print stopping for logging purposes
        print(f'stopping {camera}')

        # Get the camera object that should be stopped
        entry = CameraHandler.cameras[camera]

        # Start stopping the conversion
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

    def prepare(self):
        """Validate and check the header token if a public key is specified"""

        # If a key is specified
        if self.public_key:
            try:
                # Decode the token using the given key and the header token
                decoded = jwt.decode(self.request.headers.get('Authorization').split()[
                                     1], self.public_key, algorithms=['RS256'], audience=self.audience)

            except ValueError as exc:
                # If decoding fails, return a 401 not authorized status
                self.set_status(401)
                raise tornado.web.Finish() from exc

            # If decoding succeeds, but the scope is invalid, return 403
            if self.scope in decoded['resource_access'][self.audience]:
                self.set_status(403)
                raise tornado.web.Finish()

    def get_absolute_path(self, root, path):
        """Handle all file logic, including starting and stopping the conversion"""

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

        if extension == 'm3u8':
            # If the request is for an index file of an existing camera
            if camera in CameraHandler.cameras:
                # Get the camera object
                entry = CameraHandler.cameras[camera]

                # If there is no current conversion, start one
                if entry.conversion is None:
                    print(f'starting {camera}')

                    # see https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new
                    entry.conversion = Popen(
                        [
                            'ffmpeg', '-loglevel', 'fatal', '-rtsp_transport', 'tcp', '-i', entry.ip_adress,
                            '-map', '0:0', '-map', '0:1', '-map', '0:0', '-map', '0:1', '-map', '0:0',
                            '-map', '0:1',  # Create 3 variances of video + audio stream
                            '-profile:v', 'main', '-crf', '20', '-sc_threshold', '0', '-g', '48',
                            '-keyint_min', '48', '-c:a', 'aac', '-ar', '48000',
                            # Set common properties of the video variances
                            '-s:v:0', '640x360', '-c:v:0', self.encoding, '-b:v:0', '800k', '-maxrate',
                            '900k', '-bufsize', '1200k',  # 360p - Low bit-rate Stream
                            '-s:v:1', '854x480', '-c:v:1', self.encoding, '-b:v:1', '1425k', '-maxrate',
                            '1600k', '-bufsize', '2138k',  # 420p - Medium bit-rate Stream
                            '-s:v:2', '1280x720', '-c:v:2', self.encoding, '-b:v:2', '2850k', '-maxrate',
                            '3200k', '-bufsize', '4275k',  # 720p - High bit-rate Stream
                            '-c:a', 'copy',  # Copy original audio to the video variances
                            '-var_stream_map', 'v:0,a:0 v:1,a:1 v:2,a:2',
                            # Create the master playlist
                            '-master_pl_name', f'{camera}.m3u8',
                            '-hls_time', self.segmentSize, '-hls_list_size', self.segmentAmount,
                            '-hls_flags', 'delete_segments',
                            '-start_number', '1',  # Configure segment properties
                            f'{root}/{camera}_V%v.m3u8'
                        ]) if entry.audio else Popen([
                            'ffmpeg', '-loglevel', 'fatal', '-rtsp_transport', 'tcp', '-i', entry.ip_adress,
                            '-map', '0:0', '-map', '0:0', '-map', '0:0',
                            '-profile:v', 'main', '-crf', '20', '-sc_threshold', '0', '-g', '48', '-keyint_min', '48',
                            '-s:v:0', '640x360', '-c:v:0', self.encoding, '-b:v:0',
                            '800k', '-maxrate', '900k', '-bufsize', '1200k',
                            '-s:v:1', '854x480', '-c:v:1', self.encoding, '-b:v:1',
                            '1425k', '-maxrate', '1600k', '-bufsize', '2138k',
                            '-s:v:2', '1280x720', '-c:v:2', self.encoding, '-b:v:2',
                            '2850k', '-maxrate', '3200k', '-bufsize', '4275k',
                            '-var_stream_map', 'v:0 v:1 v:2', '-master_pl_name', f'{camera}.m3u8',
                            '-hls_time', self.segmentSize, '-hls_list_size', self.segmentAmount, '-hls_flags',
                            'delete_segments', '-start_number', '1',
                            f'{root}/{camera}_V%v.m3u8'
                        ])

                    # Wait a maximum of x seconds for the file to be created
                    for _ in range(0, self.timeoutDelay):
                        if os.path.exists(abspath):
                            break
                        time.sleep(1)

                    # If not created, stop the conversion
                    if not os.path.exists(abspath):
                        self.stop_stream(root, camera)

        # If it requests an stream file
        if extension in ('m3u8', 'ts'):
            if camera in CameraHandler.cameras:
                entry = CameraHandler.cameras[camera]

                # Cancel any current callbacks
                if entry.callback is not None:
                    entry.callback.cancel()
                    entry.callback = None

                # If there is an conversion
                if entry.conversion is not None:
                    # Reschedule a new callback to stop the stream
                    entry.callback = threading.Timer(
                        self.removeDelay, self.stop_stream, [root, camera])
                    entry.callback.start()

        return abspath
