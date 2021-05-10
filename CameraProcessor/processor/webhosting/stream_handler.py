"""File that displays the video stream on a localhost for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import time
import logging
import tornado.web
import tornado.gen
import cv2

import processor.utils.draw as draw
from processor.main import main
from processor.pipeline.process_frames import process_stream

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

        self.served_image_timestamp = time.time()

        vid_stream, detector, tracker, _ = main()
        yield process_stream(vid_stream, detector, tracker, self.when_done)

    async def when_done(self, frame_obj, tracked_boxes):
        draw.draw_tracking_boxes(frame_obj.get_frame(), tracked_boxes.get_bounding_boxes())

        # If it does get the image the frame gets encoded
        ret, jpeg = cv2.imencode('.jpg', frame_obj.get_frame())
        img = jpeg.tobytes()

        # Every .1 seconds the frame gets sent to the browser
        self.interval = .1

        try:
            self.write('--jpgboundary')
            self.write('Content-type: image/jpeg\r\n')
            self.write('Content-length: %s\r\n\r\n' % len(img))
            self.write(img)
        except RuntimeError as err:
            logging.error(f'Client disconnected, throwing the following error: {err}')

        if self.served_image_timestamp + self.interval < time.time():
            self.flush()
            self.served_image_timestamp = time.time()
