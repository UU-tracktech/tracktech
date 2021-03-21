import os
import sys
import tornado.web
import tornado.ioloop
import json
import threading
import time
import ssl
import re
from datetime import datetime
from subprocess import Popen

# Object to store camera stream information in
class Camera:
    def __init__(self, ip, audio):
        self.ip = ip
        self.conversion = None
        self.callback = None
        self.audio = audio

# Camera request handler
class cameraHandler(tornado.web.StaticFileHandler):
    cameras = {}
    segmentSize = os.environ.get('SEGMENT_SIZE') or '1'
    segmentAmount = os.environ.get('SEGMENT_AMOUNT') or '5'
    removeDelay = float(os.environ.get('REMOVE_DELAY') or '60.0')
    timeoutDelay = int(os.environ.get('TIMEOUT_DELAY') or '30')

    # Function to allow cors
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Cache-control", "no-cache")

    # Function to stop a stream
    def stop_stream(self, root, camera):
        print(f'stopping {camera}')

        # Get the entry
        entry = cameraHandler.cameras[camera]

        # Terminate the conversion
        entry.conversion.terminate()
        entry.conversion.wait(10) # Wait for the process to actually stop
        entry.conversion = None

        # Remove old files
        for file in os.listdir(root):
            if file.startswith(camera):
                os.remove(os.path.join(root, file))

    # Override function to start the stream
    def get_absolute_path(self, root, path):
        # Determine the absolute path
        abspath = os.path.abspath(os.path.join(root, path))

        match = re.search('(.*?)(?:_V.*)?\.(m3u8|ts)', path)
        camera = match.group(1)
        extension = match.group(2)
        
        # If it requests an index file
        if extension == 'm3u8':
            if camera in cameraHandler.cameras:
                entry = cameraHandler.cameras[camera]

                # If there is no current conversion, start one
                if entry.conversion is None:
                    print(f'starting {camera}')
                    
                    entry.conversion = Popen(['ffmpeg', '-loglevel', 'fatal', '-rtsp_transport', 'tcp', '-i', entry.ip,
                    '-map', '0:0','-map', '0:1', '-map', '0:0', '-map', '0:1', '-map', '0:0', '-map', '0:1', # Create 3 variances of video + audio stream
                    '-profile:v', 'main', '-crf', '20', '-sc_threshold', '0', '-g', '48', '-keyint_min', '48', '-c:a', 'aac', '-ar', '48000', # Set common properties of the video variances
                    '-s:v:0', '640x360', '-c:v:0', 'libx264', '-b:v:0', '800k', '-maxrate', '900k', '-bufsize', '1200k',    # 360p - Low bit-rate Stream
                    '-s:v:1', '854x480', '-c:v:1', 'libx264', '-b:v:1', '1425k', '-maxrate', '1600k', '-bufsize', '2138k',  # 420p - Medium bit-rate Stream
                    '-s:v:2', '1280x720', '-c:v:2', 'libx264', '-b:v:2', '2850k', '-maxrate', '3200k', '-bufsize', '4275k', # 720p - High bit-rate Stream
                    '-c:a', 'copy', # Copy original audio to the video variances
                    '-var_stream_map', 'v:0,a:0 v:1,a:1 v:2,a:2',
                    '-master_pl_name', f'{camera}.m3u8',  # Create the master playlist
                    '-hls_time', self.segmentSize, '-hls_list_size', self.segmentAmount, '-hls_flags', 'delete_segments','-start_number', '1',  # Configure segment properties
                     f'{root}/{camera}_V%v.m3u8']) if entry.audio else Popen(['ffmpeg', '-loglevel', 'fatal', '-rtsp_transport', 'tcp', '-i', entry.ip,
                    '-map', '0:0', '-map', '0:0', '-map', '0:0',
                    '-profile:v', 'main', '-crf', '20', '-sc_threshold', '0', '-g', '48', '-keyint_min', '48',
                    '-s:v:0', '640x360', '-c:v:0', 'libx264', '-b:v:0', '800k', '-maxrate', '900k', '-bufsize', '1200k',
                    '-s:v:1', '854x480', '-c:v:1', 'libx264', '-b:v:1', '1425k', '-maxrate', '1600k', '-bufsize', '2138k',
                    '-s:v:2', '1280x720', '-c:v:2', 'libx264', '-b:v:2', '2850k', '-maxrate', '3200k', '-bufsize', '4275k',
                    '-var_stream_map', 'v:0 v:1 v:2', '-master_pl_name', f'{camera}.m3u8',
                    '-hls_time', self.segmentSize, '-hls_list_size', self.segmentAmount, '-hls_flags', 'delete_segments', '-start_number', '1',
                     f'{root}/{camera}_V%v.m3u8'])

                    # Wait a maximum of x seconds for the file to be created
                    for _ in range(0, self.timeoutDelay):
                        if os.path.exists(abspath) : break
                        time.sleep(1)

                    # If not created, stop the conversion
                    if not os.path.exists(abspath): self.stop_stream(root, camera)
        
        # If it requests an stream file
        if extension == 'm3u8' or extension == 'ts':
            if camera in cameraHandler.cameras:
                entry = cameraHandler.cameras[camera]

                # Cancel any current callbacks
                if entry.callback is not None:
                    entry.callback.cancel()
                    entry.callback = None

                # If there is an conversion
                if entry.conversion is not None :
                    # Reschedule a new callback to stop the stream
                    entry.callback = threading.Timer(self.removeDelay, self.stop_stream, [root, camera])
                    entry.callback.start()

        return abspath


if __name__ == "__main__":
    print('starting server')

    # Read the config file
    configFile = open(sys.argv[1], "r")
    configJson = json.loads(configFile.read())
    configFile.close()

    # Save the cameras in the stat
    cameraHandler.cameras = {camera["Name"]: Camera(camera["Ip"], camera["Audio"]) for camera in configJson}

    # Get ssl ready, if provided in the environment variables
    cert = os.environ.get('SSL_CERT')
    key = os.environ.get('SSL_KEY')
    use_tls = cert is not None and key is not None

    # Create a web application
    app = tornado.web.Application(
        [(r'/(.*)', cameraHandler, {'path': 'streams'})])

    if use_tls:
        # Create a ssl context
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(cert, key)

        # Create a http server, with optional ssl.
        http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)
        http_server.listen(443)
        print('listening on port 443 over https')

    else:
        # Create a http server, with optional ssl.
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(80)
        print('listening on port 80 over http')

    # Start io loop
    tornado.ioloop.IOLoop.current().start()
