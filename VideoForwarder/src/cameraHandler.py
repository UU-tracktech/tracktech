"""
The request handler that serves the actual HLS index and segment files
It handles authentication/authorization and makes sure conversion processes of cameras are started and stopped
"""

import os
import tornado.web
import re
import threading
import time
from subprocess import Popen
import jwt

from camera import Camera


class CameraHandler(tornado.web.StaticFileHandler):
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

    publicKey = None
    """The public key used to validate tokens"""

    def initialize(self, path):
        """Set the root path and load the public key from application settings, run at the start of every request"""

        self.root = path
        """Needed for the library"""

        self.publicKey = self.application.settings.get('publicKey')
        """Load the public key from application settings"""

    def set_default_headers(self):
        """Set the headers to allow cors and disable caching"""

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Cache-control", "no-store")

    def stop_stream(self, root, camera):
        """Function to stop a given camera stream, will be called once a stream is no longer used for a specific amount of time"""

        print(f'stopping {camera}')
        """Print stopping for loggin purposes"""

        entry = CameraHandler.cameras[camera]
        """Get the camera object that should be stopped"""

        entry.conversion.terminate()
        """Start stopping the conversion"""
        try:
            entry.conversion.wait(60)
            """Wait a few seconds for it stop, so it does not lock any files"""
        except Popen.TimeoutExpired:
            """Handle a timeout exception if the process does not stop"""
            pass
        finally:
            entry.conversion = None
            """Remove the conversion"""

            for file in os.listdir(root):
                if file.startswith(camera):
                    os.remove(os.path.join(root, file))
            """Remove the old segment and index files"""

    def prepare(self):
        """Validate and check the header token if a public key is specified"""

        if self.publicKey is not None:
            """If a key is specified"""
]
            try:
                decoded = jwt.decode(self.request.headers.get('Authorization').split()[
                                     1], self.publicKey, algorithms=['RS256'], audience=self.audience)
                """Decode the token using the given key and the header token"""

            except:
                self.set_status(401)
                raise tornado.web.Finish()
                """If decoding fails, return a 401 status"""

            if self.scope in decoded['resource_access'][self.audience]:
                self.set_status(403)
                raise tornado.web.Finish()
                """If decoding succeeds, but the scope is invalid, return 403"""

    def get_absolute_path(self, root, path):
        """Handle all file logic, including starting and stopping the conversion"""

        abspath = os.path.abspath(os.path.join(root, path))
        """Get the path on the file system"""

        match = re.search('(.*?)(?:_V.*)?\.(m3u8|ts)', path)
        """Regex the file path"""

        if match is None:
            return abspath
        """If there is no match, return the path as usual"""

        camera = match.group(1)
        extension = match.group(2)
        """Otherwise, grab the camera and extension information"""

        if extension == 'm3u8':
            if camera in CameraHandler.cameras:
                """If the request is for an index file of an existing camera"""

                entry = CameraHandler.cameras[camera]
                """Get the camera object"""

                # If there is no current conversion, start one
                if entry.conversion is None:
                    print(f'starting {camera}')

                    # see https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new for hardware limits
                    entry.conversion = Popen(
                        [
                            'ffmpeg', '-loglevel', 'fatal', '-rtsp_transport', 'tcp', '-i', entry.ip,
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
                            'ffmpeg', '-loglevel', 'fatal', '-rtsp_transport', 'tcp', '-i', entry.ip,
                            '-map', '0:0', '-map', '0:0', '-map', '0:0',
                            '-profile:v', 'main', '-crf', '20', '-sc_threshold', '0', '-g', '48', '-keyint_min', '48',
                            '-s:v:0', '640x360', '-c:v:0', self.encoding, '-b:v:0', '800k', '-maxrate', '900k', '-bufsize',
                            '1200k',
                            '-s:v:1', '854x480', '-c:v:1', self.encoding, '-b:v:1', '1425k', '-maxrate', '1600k', '-bufsize',
                            '2138k',
                            '-s:v:2', '1280x720', '-c:v:2', self.encoding, '-b:v:2', '2850k', '-maxrate', '3200k', '-bufsize',
                            '4275k',
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
        if extension == 'm3u8' or extension == 'ts':
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
