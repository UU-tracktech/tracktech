import cv2
import logging
from input.custom_capture import ICapture


class VideoCapture(ICapture):

    #Default path is the path to venice.mp4
    def __init__(self, path='/data/videos/venice.mp4'):
        logging.info("Opening video from path")
        self.cap = cv2.VideoCapture(path)
        logging.info("Successfully opened video file")

    # Check if video stream is stopped, either due to error or eof
    def stopped(self):
        return not self.cap.isOpened()

    # Releases the video
    def close(self):
        self.cap.release()

    # Gets the next frame of the video buffer
    def get_next_frame(self):
        return self.cap.read()

    #Returns the amount of total frames in the video
    def get_vid_length(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_COUNT)