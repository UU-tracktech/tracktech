"""Contains camera capture class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import time
import logging
from cv2 import VideoCapture

from processor.input.icapture import ICapture
from processor.data_object.frame_obj import FrameObj


class CamCapture(ICapture):
    """Captures video from a webcam or other connected camera on the computer.

    Attributes:
        cap (cv2.VideoCapture): Capture that serves webcam frame one by one.
    """
    def __init__(self):
        """Opens capture that connects to webcam.
        """
        logging.info('connecting to webcam')
        self.cap = VideoCapture(0)

    def opened(self):
        """Checks if webcam is still opened.

        Returns:
            bool: whether webcam is still on.
        """
        return self.cap.isOpened()

    def close(self):
        """Releases webcam."""
        self.cap.release()

    def get_next_frame(self):
        """Gets the next frame from the capture object.

        Returns:
            bool, numpy.ndarray: Whether a next frame was found and its frame.
        """
        ret, frame = self.cap.read(0)
        return ret, FrameObj(frame, time.time())
