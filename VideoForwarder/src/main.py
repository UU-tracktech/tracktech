import os
import sys
import tornado.web
import tornado.ioloop
import json
import threading
from datetime import datetime
from subprocess import Popen

# Object to store camera stream information in
class Camera:
    def __init__(self, ip, conversion): 
        self.ip = ip
        self.conversion = conversion
        self.callback = None

# Camera request handler
class cameraHandler(tornado.web.StaticFileHandler):
    cameras = {}
    segmentSize = os.environ.get('SEGMENT_SIZE') or '10'
    segmentAmount = os.environ.get('SEGMENT_AMOUNT') or '5'
    timeoutDelay = os.environ.get('TIMEOUT_DELAY') or '30'
    
    # Function to stop a stream
    def stop_stream(self, root, camera):
        # Get the entry
        entry = cameraHandler.cameras[camera]

        # Terminate the conversion
        entry.conversion.terminate()
        entry.conversion = None

        # Remove old files
        for file in os.listdir(root):
            if file.startswith(camera):
                os.remove(os.path.join(root, file))

    # Override function to start the stream 
    def get_absolute_path(self, root, path):
        # Determine the absolute path
        abspath = os.path.abspath(os.path.join(root, path))

        # If it requests an index file
        if path.endswith('.m3u8'):
            camera = path.replace('.m3u8','')
            if camera in cameraHandler.cameras:
                entry = cameraHandler.cameras[camera]

                # If there is no current conversion, start one
                if entry.conversion is None:
                    entry.conversion = Popen(['ffmpeg','-rtsp_transport','tcp','-i',entry.ip,'-r','100','-crf','25','-preset','faster','-maxrate','500k','-bufsize','1500k','-c:v','libx264','-hls_time',self.segmentSize,'-hls_list_size',self.segmentAmount,'-hls_flags','delete_segments','-start_number','1','-rtsp_transport','tcp', abspath])      
        
        # If it requests an stream file
        if path.endswith('.m3u8') or path.endswith('.ts'):
            camera = path.replace('.m3u8','').replace('.ts','')
            if camera in cameraHandler.cameras:
                entry = cameraHandler.cameras[camera]

                # Cancel any current callbacks
                if entry.callback is not None:
                    entry.callback.cancel()

                # Reschedule a new callback to stop the stream
                entry.callback = threading.Timer(self.timeoutDelay, self.stop_stream, [root, camera])
                entry.callback.start()

        return abspath

if __name__ == "__main__":
    # Read the config file
    configFile = open(sys.argv[1], "r")
    configJson = json.loads(configFile.read())
    configFile.close()

    # Save the cameras in the stat
    cameraHandler.cameras = {camera["Name"]:Camera(camera["Ip"],None) for camera in configJson}

    # Start tornado
    app = tornado.web.Application([ 
        (r"/(.*)", cameraHandler, {'path': 'streams'})
    ])
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()