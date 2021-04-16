import os
import tornado.web
import re
import threading
import time
from subprocess import Popen
import jwt

from camera import Camera


# Camera request handler
class CameraHandler(tornado.web.StaticFileHandler):
    cameras = {}
    segmentSize = os.environ.get('SEGMENT_SIZE') or '1'
    segmentAmount = os.environ.get('SEGMENT_AMOUNT') or '5'
    removeDelay = float(os.environ.get('REMOVE_DELAY') or '60.0')
    timeoutDelay = int(os.environ.get('TIMEOUT_DELAY') or '30')

    encoding = os.environ['ENCODING']

    secret = os.environ.get('JWT_PUBLIC_SECRET')
    audience = os.environ.get('TOKEN_AUDIENCE')
    scope = os.environ.get('TOKEN_SCOPE')
    publicKey = None

    def initialize(self, path):
        self.root = path

        # retrieve the public key
        self.publicKey = self.application.settings.get('publicKey') 

    # Function to allow cors
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Cache-control", "no-store")

    # Function to stop a stream
    def stop_stream(self, root, camera):
        print(f'stopping {camera}')

        # Get the entry
        entry = CameraHandler.cameras[camera]

        # Terminate the conversion
        entry.conversion.terminate()
        try:
            entry.conversion.wait(10)  # Wait for the process to actually stop
        except TimeoutExpired:
            pass
        finally:
            entry.conversion = None

            # Remove old files
            for file in os.listdir(root):
                if file.startswith(camera):
                    os.remove(os.path.join(root, file))

    # To authenticate
    def prepare(self):
        # If auth is enabled
        if self.publicKey is not None:

            # Try to decode the token using the public key
            try:
                decoded = jwt.decode(self.request.headers.get('Authorization').split()[
                                     1], self.publicKey, algorithms=['RS256'], audience=self.audience)

            # If decoding fails, return not authorized
            except:
                self.set_status(401)
                raise tornado.web.Finish()

            # If decoding succeeds, but the required scope is missing, return not authorized
            if self.scope in decoded['resource_access'][self.audience]:
                self.set_status(403)
                raise tornado.web.Finish()

            # Continue otherwise
            return

    # Override function to start the stream
    def get_absolute_path(self, root, path):
        # Determine the absolute path
        abspath = os.path.abspath(os.path.join(root, path))

        match = re.search('(.*?)(?:_V.*)?\.(m3u8|ts)', path)

        if match is None:
            return abspath

        camera = match.group(1)
        extension = match.group(2)

        # If it requests an index file
        if extension == 'm3u8':
            if camera in CameraHandler.cameras:
                entry = CameraHandler.cameras[camera]

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
