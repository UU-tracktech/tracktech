"""Contains the video capture class

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import time
import logging
import cv2
from processor.input.icapture import ICapture
from processor.data_object.frame_obj import FrameObj


class VideoCapture(ICapture):
    """ Captures video from a video file on the system.

    Attributes:
        cap (cv2.VideoCapture): VideoCapture that reads stream as frames.
        __nr_frames (int): Number of frames of video.
        __current_frame_nr (int): Index number of current frame.
    """
    # Default path is the path to venice.mp4
    def __init__(self, path='/data/videos/test.mp4'):
        """Create a VideoCapture given a path.

        Args:
            path (str): path to the video.
        """
        # Open VideoCapture
        logging.info(f"Opening video from path: {path}")
        self.cap = cv2.VideoCapture(path)
        logging.info("Successfully opened video file")

        # Frame counter to stop at last frame
        self.__nr_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.__current_frame_nr = 0
        logging.info(f"Video has {self.__nr_frames} frames")

    def opened(self):
        """Check if the video is still opened.

        Returns:
            A boolean indicating if video is opened.
        """
        # Frame is beyond what current frame is
        if self.__current_frame_nr >= self.__nr_frames:
            return False

        return self.cap.isOpened()

    def close(self):
        """Close video capture."""
        self.__current_frame_nr = self.__nr_frames
        self.cap.release()

    def get_next_frame(self):
        """Gets the next frame of the video.

        Returns (bool, FrameObj):
            Boolean indicating if next frame was returned.
            FrameObj containing frame and an empty datetime.
        """
        # Return False if the capture was closed
        if not self.opened():
            return False, None

        self.__current_frame_nr += 1
        ret, frame = self.cap.read()
        return ret, FrameObj(frame, time.time())
