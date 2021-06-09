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
        cap (cv2.VideoCapture): Capture that serves webcam frames one by one.
    """
    def __init__(self, device_nr):
        """Opens capture that connects to webcam.

        Args:
            device_nr (int): Number of the device to take the recorded data from.
        """
        logging.info(f'Connecting to webcam on device {device_nr}')
        self.cap = VideoCapture(device_nr)

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
