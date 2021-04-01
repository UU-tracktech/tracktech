import cv2
import ffmpeg
import threading
import time
import logging
from typing import List
from src.input.icapture import ICapture


class HlsCapture(ICapture):
    """Implementation of the ICapture class which handles an HLS stream with timestamps.

    Main thread runs the implementation with open, close and getting the next frame.
    Seperate thread runs the reading loop, which reads the next frame at a constant rate.
    Another thread gets the time stamp of the stream once and going from there.
    """
    def __init__(self, hls_url='http://81.83.10.9:8001/mjpg/video.mjpg'):
        """Initiates the capture object with a hls url and starts reading frames

        Default hls_url is of a public stream that is available 24/7

        Args:
            hls_url: Url the videocapture has to connect to
        """
        # Stream related properties
        self.hls_url = hls_url
        self.cap = None

        # Time stamps
        self.start_time_stamp = 0
        self.frame_time_stamp = 0
        self.last_frame_time_stamp = 0

        # Time
        self.thread_start_time = 0
        self.wait_ms = 0

        # Frame numbers
        self.current_frame = 0
        self.current_frame_nr = 0

        # Create thread that syncs streams
        self.t = threading.Thread(target=self.sync)
        self.t.daemon = True
        self.t.start()

    def opened(self) -> bool:
        """Check whether the current capture object is still opened

        Returns:
            Whether stream is still openened at this point of time
        """
        return self.cap.isOpened()

    # When everything is done release the capture
    def close(self) -> None:
        """Closes the capture object and the thread that is responsible for serving the current frame
        """
        logging.info('HLS stream closing')
        self.t.join()
        self.cap.release()

    def get_next_frame(self) -> (bool, List[List[int]], float):
        """Gets the next frame from the hls stream

        Returns:
            Boolean whether a new frame has been returned compared to the previous one.
            Frame which is the current frame to be processed.
            Timestamp of the current frame given back by the method.
        """
        # Frame is not different from the last one
        if self.frame_time_stamp == self.last_frame_time_stamp:
            return False, None, None
        self.last_frame_time_stamp = self.frame_time_stamp
        return True, self.current_frame, self.frame_time_stamp

    def read(self) -> None:
        """Method that runs in seperate thread that goes through the frames of the stream at a consistent pace

        Reads frames at frame rate of the stream and puts them in self.current_frame
        Calculates at what time the next frame is expected and waits that long
        """
        while True:
            # Reads next frame
            ret, self.current_frame = self.cap.read()

            # If frame was not yet ready
            if not ret:
                continue
            self.current_frame_nr += 1

            # What is the wait time until next frame has to be prepared
            expected_next_frame_time = self.wait_ms * self.current_frame_nr
            time_into_stream = time.time() - self.thread_start_time
            wait_time = int(expected_next_frame_time - time_into_stream * 1000)

            # Saves timestamp and waits calculated amount
            self.frame_time_stamp = self.hls_start_time_stamp + time_into_stream

            # Next frame should already have been read
            if wait_time <= 0:
                continue

            cv2.waitKey(wait_time)

    def sync(self) -> None:
        """Method to instantiate the video connection with the HLS stream

        Makes a separate thread to request meta-data and sets the default values for the variables
        """
        logging.info('connecting to HLS stream')

        # Starts a separate thread to request meta-data
        threading.Thread(target=self.get_meta_data).start()

        # Instantiates the connection with the hls stream
        self.cap = cv2.VideoCapture(self.hls_url)

        # Saves the current time of a successful established connection
        self.thread_start_time = time.time()

        logging.info('opened HLS stream')

        # Get the FPS of the hls stream and turn it into a delay of when each frame should be displayed
        self.wait_ms = 1000 / self.cap.get(cv2.CAP_PROP_FPS)
        self.read()

    def get_meta_data(self) -> None:
        """Make a http request with ffmpeg to get the meta-data of the HLS stream,
        """
        # extract the start_time from the meta-data to get the absolute segment time
        self.hls_start_time_stamp = float(ffmpeg.probe(self.hls_url)['format']['start_time'])
