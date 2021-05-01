"""File that displays the video stream on a localhost for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import time
import logging
import os
import sys
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpserver
import tornado.process
import tornado.template
import tornado.gen
import cv2

from processor.input.hls_capture import HlsCapture

logging.basicConfig(filename='localhost.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# Tornado example gotten from: https://github.com/wildfios/Tornado-mjpeg-streamer-python
# Combined with: https://github.com/wildfios/Tornado-mjpeg-streamer-python/issues/7


class StreamHandler(tornado.web.RequestHandler):
    """Handler for the frame stream."""
    server_image_timestamp = 0

    @tornado.gen.coroutine
    def get(self):
        """Get request handler for the webpage to show video stream."""
        # Sets headers of the handler
        logging.info('set headers')
        self.set_header('Cache-Control',
                        'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary=--jpgboundary')
        self.set_header('Connection', 'close')

        served_image_timestamp = time.time()
        my_boundary = '--jpgboundary'

        # Create capture and start read loop
        capture = HlsCapture()
        while capture.opened():
            # Get frame
            ret, frame_obj = capture.get_next_frame()
            if not ret:
                continue
            # If it does get the image the frame gets encoded
            ret, jpeg = cv2.imencode('.jpg', frame_obj.get_frame())
            img = jpeg.tobytes()

            # Every .1 seconds the frame gets sent to the browser
            interval = 0.1
            if served_image_timestamp + interval < time.time():
                self.write(my_boundary)
                self.write('Content-type: image/jpeg\r\n')
                self.write('Content-length: %s\r\n\r\n' % len(img))
                self.write(img)
                served_image_timestamp = time.time()

            try:
                self.flush()
            except Exception as err:
                raise Exception('connection lost with client') from err
