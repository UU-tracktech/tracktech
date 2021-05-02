"""Contains the HlsCapture class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import threading
import sys
import time
import logging
import ffmpeg
import cv2

from processor.input.icapture import ICapture
from processor.data_object.frame_obj import FrameObj


class HlsCapture(ICapture):
    """Implementation of the ICapture class which handles an HLS stream with timestamps.

    Main thread runs the implementation with open, close and getting the next frame.
    Separate thread runs the reading loop, which reads the next frame at a constant rate.
    Another thread gets the time stamp of the stream once and going from there.

    Attributes:
        hls_url (str): Url of hls stream.
        cap (cv2.VideoCapture): Capture object that serves frame one by one.
        __cap_initialized (bool): Whether the capture is initialized.

        __start_time_stamp (float): Start time of capture object.
        __frame_time_stamp (float): Time stamp of current frame.
        __last_frame_time_stamp (float): Time stamp of previous frame.
        __hls_start_time_stamp (float): Start time of hls stream.

        __thread_start_time (float): Start time of thread.
        __wait_ms (float): Time between frames in ms.

        __current_frame (numpy.ndarray): Current frame.
        __current_frame_nr (int): Current frame index.

        __thread_running (bool): Whether separate thread is running.

        __reading_thread (Thread): Contains thread that reads.

        __probe_done (bool): Whether ffmpeg probe is done.
        __found_stream (bool): Whether stream was found.

    """
    def __init__(self, hls_url='http://81.83.10.9:8001/mjpg/video.mjpg'):
        """Initiates the capture object with a hls url and starts reading frames.

        Default hls_url is of a public stream that is available 24/7.

        Args:
            hls_url: Url the videocapture has to connect to.
        """

        # Stream related properties
        self.hls_url = hls_url
        self.cap = None
        self.__cap_initialized = False

        # Time stamps
        self.__start_time_stamp = 0
        self.__frame_time_stamp = 0
        self.__last_frame_time_stamp = 0
        self.__hls_start_time_stamp = 0

        # Time
        self.__thread_start_time = 0
        self.__wait_ms = 0

        # Frame numbers
        self.__current_frame = None
        self.__current_frame_nr = 0

        # Tells thread they should keep running
        self.__thread_running = False

        # Thread
        self.__reading_thread = None

        # Reconnect with timeout
        self.__probe_done = False
        self.__found_stream = False
        tries_left = 10

        # Sleep is essential so processor has a prepared self.cap
        while not self.__cap_initialized and not self.__found_stream and tries_left > 0:
            self.__probe_done = False
            self.__connect_to_stream()

            # Probe did not yet finish
            while not self.__probe_done:
                continue

            time.sleep(1)
            tries_left -= 1

        # Raise error when capture is never created in other thread
        if not self.__found_stream:
            logging.error("cv2.VideoCapture probably raised exception")
            raise TimeoutError("HLS Capture never opened")

    def __connect_to_stream(self):
        """Connects to hls stream in separate thread."""
        # Create thread that reads streams
        self.__reading_thread = threading.Thread(target=self.sync)
        self.__reading_thread.daemon = True
        self.__reading_thread.start()

    def opened(self):
        """Check whether the current capture object is still opened.

        Returns (bool):
            Whether stream is still opened at this point of time.
        """
        if self.cap:
            return self.cap.isOpened()
        return False

    def close(self):
        """Closes the capture object and the thread that is responsible for serving the current frame."""
        logging.info('HLS stream closing')
        logging.info("Joining thread")
        self.__thread_running = False
        self.__reading_thread.join()
        logging.info("Thread joined")

    def get_next_frame(self):
        """Gets the next frame from the hls stream.

        Returns (bool, FrameObj):
            Boolean whether a new frame has been returned compared to the previous one.
            Frame Object containing the next frame.
        """
        # Frame is not different from the last one
        if self.__frame_time_stamp == self.__last_frame_time_stamp:
            return False, None

        self.__last_frame_time_stamp = self.__frame_time_stamp
        return True, FrameObj(self.__current_frame, self.__frame_time_stamp)

    def __read(self):
        """Method that runs in separate thread that goes through the frames of the stream at a consistent pace.

        Reads frames at frame rate of the stream and puts them in self.current_frame.
        Calculates at what time the next frame is expected and waits that long.
        """
        while self.__thread_running:
            # Reads next frame
            ret, self.__current_frame = self.cap.read()

            # If frame was not yet ready
            if not ret:
                continue

            self.__current_frame_nr += 1

            # What is the wait time until next frame has to be prepared
            expected_next_frame_time = self.__wait_ms * self.__current_frame_nr
            time_into_stream = time.time() - self.__thread_start_time
            wait_time = int(expected_next_frame_time - time_into_stream * 1000)

            # Saves timestamp and waits calculated amount
            self.__frame_time_stamp = self.__hls_start_time_stamp + time_into_stream

            # Next frame should already have been read
            if wait_time <= 0:
                continue

            cv2.waitKey(wait_time)

        # Release cap in thread that uses it to prevent following bug:
        # Other thread stops cap whilst current thread is still reading the next frame
        self.cap.release()
        logging.info("Capture is released")

    def sync(self):
        """Method to instantiate the video connection with the HLS stream.

        Makes a separate thread to request meta-data and sets the default values for the variables.
        """
        logging.info(f'Connecting to HLS stream, url: {self.hls_url}')
        self.cap = None

        meta_thread = threading.Thread(target=self.__get_meta_data)
        meta_thread.daemon = True
        meta_thread.start()

        # Instantiates the connection with the hls stream
        self.cap = cv2.VideoCapture(self.hls_url)

        # Make sure thread has finished before starting main loop
        meta_thread.join()

        # Exit thread if stream was not found
        if not self.__found_stream:
            self.cap.release()
            logging.warning('Stream was not found')
            sys.exit()

        # Saves the current time of a successful established connection
        self.__thread_start_time = time.time()

        # Exit because capture did not start correctly
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            logging.warning('Capture not found correctly')
            sys.exit()

        # How much time has to get awaited between frames
        self.__wait_ms = 1000 / fps

        # Thread should continue running since it is initialized correctly
        self.__thread_running = True
        logging.info("Thread started successfully!")

        # Done with probing and cap is initialized
        self.__cap_initialized = True
        self.__probe_done = True

        self.__read()

    # pylint: disable=protected-access
    def __get_meta_data(self):
        """Make a http request with ffmpeg to get the meta-data of the HLS stream."""
        # extract the start_time from the meta-data to get the absolute segment time
        logging.info('Retrieving meta data from HLS stream')
        # Probe HLS stream link
        try:
            # pylint: disable=no-member
            meta_data = ffmpeg.probe(self.hls_url)
            # pylint: enable=no-member
            self.__hls_start_time_stamp = float(meta_data['format']['start_time'])

        # Ffmpeg probe error
        except ffmpeg._run.Error as error:
            logging.error(f'ffmpeg could not find stream, giving the following error: {error}')
            return

        # Json did not contain key
        except KeyError as key_error:
            logging.warning(f'Json does not contain keys for {key_error}')

        self.__found_stream = True
