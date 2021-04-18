import logging
from typing import List
from cv2 import VideoCapture
from processor.input.icapture import ICapture

vcap = VideoCapture(0)


class CamCapture(ICapture):
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
