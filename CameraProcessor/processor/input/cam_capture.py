"""Contains camera capture class

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import logging
from typing import List
from cv2 import VideoCapture
from processor.input.icapture import ICapture

vcap = VideoCapture(0)


class CamCapture(ICapture):
    """ Captures video from a webcam or other connected camera on the computer

    """
    def __init__(self):
        """Opens capture that connects to webcam.
        """
        logging.info('connecting to webcam')
        self.cap = vcap

    def opened(self) -> bool:
        """Checks if webcam is still opened.

        Returns:
            Boolean whether webcam is still on.
        """
        return self.cap.isOpened()

    def close(self) -> None:
        """Releases webcam
        """
        self.cap.release()

    def get_next_frame(self) -> (bool, List[List[int]]):
        """Gets the next frame from the capture object.

        Returns:
            Boolean whether a next frame was found
            Next webcam frame.
        """
        return *self.cap.read(), None

    def get_capture_length(self) -> int:
        """Returns None, because webcam streams
        are theoretically infinite"""
        return None
