"""File that displays the video stream on a localhost for testing with docker.

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
from processor.pipeline.process_frames import prepare_stream, process_stream

# Tornado example gotten from: https://github.com/wildfios/Tornado-mjpeg-streamer-python
# Combined with: https://github.com/wildfios/Tornado-mjpeg-streamer-python/issues/7


# pylint: disable=attribute-defined-outside-init
class StreamHandler(tornado.web.RequestHandler):
    """Streamhandler is for the tornado localhost page. It serves JPG images to the client

    Attributes:
        __previous_flush_timestamp (float): Timestamp of the previous flush
        __flush_interval (float): Time inbetween flushes
    """
    @tornado.gen.coroutine
    def get(self):
        """Get request handler for the webpage to show video stream."""
        # Sets headers of the stream handler
        logging.info('set headers')
        self.set_header('Cache-Control',
                        'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary=--jpgboundary')
        self.set_header('Connection', 'close')

        # Timing of last flush
        self.__previous_flush_timestamp = time.time()

        # Every .1 seconds the buffer gets flushed
        self.__flush_interval = .1

        # Get the objects needed for process_stream and starts the function
        vid_stream, detector, tracker, _ = prepare_stream()
        yield process_stream(vid_stream, detector, tracker, self.frame_processed)

    async def frame_processed(self, frame_obj, tracked_boxes):
        """When the frame got processed, this function gets called to put it in the buffer

        Args:
            frame_obj (FrameObj): Frame object containing the d
            tracked_boxes (Boundingboxes): The tracked boxes from the frame processing loop
        """
        draw.draw_tracking_boxes(frame_obj.get_frame(), tracked_boxes.get_bounding_boxes())

        # Encode the frame to jpg format
        ret, jpeg = cv2.imencode('.jpg', frame_obj.get_frame())
        img = jpeg.tobytes()

        # Write to the buffer
        try:
            self.write('--jpgboundary')
            self.write('Content-type: image/jpeg\r\n')
            self.write('Content-length: %s\r\n\r\n' % len(img))
            self.write(img)
        # Connection lost
        except RuntimeError as err:
            logging.error(f'Client disconnected, throwing the following error: {err}')

        # If it is time to flush the buffer again
        if self.__previous_flush_timestamp + self.__flush_interval < time.time():
            self.flush()
            self.__previous_flush_timestamp = time.time()
