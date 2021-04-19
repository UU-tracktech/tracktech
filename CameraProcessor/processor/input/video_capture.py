import logging
import cv2
from processor.input.icapture import ICapture


class VideoCapture(ICapture):
    # Default path is the path to venice.mp4
    def __init__(self, path='/data/videos/test.mp4'):
        """

        Args:
            path: path to the video
        """
        logging.info(f"Opening video from path: {path}")
        self.cap = cv2.VideoCapture(path)
        logging.info("Successfully opened video file")
        logging.info(f"Video has {self.get_capture_length()} frames")

    def opened(self):
        """Check if the video is still opened

        Returns:
            A boolean indicating if video is opened

        """
        return self.cap.isOpened()

    def close(self):
        """Close video capture

        """
        self.cap.release()

    def get_next_frame(self):
        """Gets the next frame of the video

        Returns:
            - A boolean indicating if next frame was returned
            - an image object, in the form of a matrix of integers
        """
        return *self.cap.read(), None

    def get_capture_length(self):
        """Returns the amount of total frames in the video

        Returns:
            An int indicating the amount of frames in the video

        """
        return self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
