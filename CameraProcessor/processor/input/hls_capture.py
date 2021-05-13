"""Contains the HlsCapture class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import time
import logging
import kthread
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
        fps (int): FPS of the stream

        __start_time_stamp (float): Start time of capture object.
        __frame_time_stamp (float): Time stamp of current frame.
        __last_frame_time_stamp (float): Time stamp of previous frame.
        __hls_start_time_stamp (float): Start time of hls stream.

        __thread_start_time (float): Start time of thread.
        __wait_ms (float): Time between frames in ms

        __current_frame (numpy.ndarray): Current frame.

        __previous_time (float): a time float to determine the time diff between frame readings.
        __timeout (int): an integer for timeout in seconds (used as float).
        __grace_period (int): an integer denoting a grace period at the start before we check for timeout.

        __thread_running (bool): bool denoting whether reading thread is active or activating.

        __reading_thread (Thread): Contains thread that reads.
        __reconnect_thread (Thread): Contains thread that attempts to reconnect if connection was closed unexpectedly

        __reconnecting (bool): Boolean indicating reconnect procedure must be started
        __drop_reconnect(bool): Boolean indicating the reconnect thread can be closed
        __found_stream (bool): Boolean indicating whether stream was found.

    """
    def __init__(self, hls_url='http://81.83.10.9:8001/mjpg/video.mjpg'):
        """Initiates the capture object with a hls url and starts reading frames.

        Default hls_url is of a public stream that is available 24/7.

        Args:
            hls_url: Url the videocapture has to connect to.
        """

        # Stream related properties
        self.hls_url = hls_url
        self.fps = 0

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

        # Tells thread they should keep running
        self.__thread_running = False

        # Timeout times
        self.__previous_time = time.time()
        self.__timeout = 5
        self.__grace_period = 10

        # Thread
        self.__reading_thread = None
        self.__reconnect_thread = None

        # Reconnect with timeout
        self.__reconnecting = False
        self.__drop_reconnect = False
        self.__found_stream = False

        self.__connect_to_stream()

    def opened(self):
        """Check whether the current capture object is still opened.

        Returns (bool):
            Whether stream is still opened at this point of time.
        """
        return self.__thread_running

    def close(self):
        """Closes the capture object and the thread that is responsible for serving the current frame."""
        logging.info('HLS stream closing')
        logging.info("Joining threads")

        # Join the reading thread
        self.__thread_running = False
        self.__reading_thread.join()

        # Join the reconnecting thread
        self.__drop_reconnect = True
        self.__reconnect_thread.join()
        logging.info("Threads joined")

    def get_next_frame(self):
        """Gets the next frame from the hls stream.

        Returns (bool, FrameObj):
            Boolean whether a new frame has been returned compared to the previous one.
            Frame Object containing the next frame.
        """

        diff_time = time.time() - self.__previous_time
        self.__previous_time = time.time()

        # Return False if the capture was flagged to close
        if not self.__thread_running or self.__reconnecting:
            return False, None

        # Frame is not different from the last one
        if self.__frame_time_stamp == self.__last_frame_time_stamp:
            if self.__grace_period > 0:
                self.__grace_period -= diff_time
            else:
                self.__timeout -= diff_time
                # If the connection was dropped due to timeout, we will try to reconnect
                if self.__timeout < 0:
                    self.__reconnecting = True
                    self.__timeout = 5
                    self.__grace_period = 10
                    logging.info("Connection timed out")
            return False, None

        self.__timeout = 5

        self.__last_frame_time_stamp = self.__frame_time_stamp
        return True, FrameObj(self.__current_frame, self.__frame_time_stamp)

    def __read(self, cap, thread_start_time, hls_start_time_stamp, wait_ms):
        """Method that runs in separate thread that goes through the frames of the stream at a consistent pace.

        Reads frames at frame rate of the stream and puts them in self.current_frame.
        Calculates at what time the next frame is expected and waits that long.
        """
        # Set a timeout, in seconds
        current_frame_nr = 0
        while self.__thread_running and not self.__reconnecting:
            # Reads next frame
            try:
                ret, self.__current_frame = cap.read()
            except SystemExit as error:
                logging.warning("Capture read has been blocked")
                raise TimeoutError("Capture read has been blocked.") from error

            # If frame was not yet ready
            if not ret:
                continue

            current_frame_nr += 1

            # What is the wait time until next frame has to be prepared
            expected_next_frame_time = wait_ms * current_frame_nr
            time_into_stream = time.time() - thread_start_time
            wait_time = int(expected_next_frame_time - time_into_stream * 1000)

            # Saves timestamp and waits calculated amount
            self.__frame_time_stamp = hls_start_time_stamp + time_into_stream

            # Next frame should already have been read
            if wait_time <= 0:
                continue

            cv2.waitKey(wait_time)

    def sync(self):
        """Method to instantiate the video connection with the HLS stream.

        Makes a separate thread to request meta-data and sets the default values for the variables. Then instantiates
        the reading and reconnection thread.

        Returns:
            Bool: indicating a success or failure of setting up the capture and syncing the meta data
        """
        logging.info(f'Connecting to HLS stream, url: {self.hls_url}')

        # Creating meta thread for meta data collection
        self.__found_stream = False
        meta_thread = kthread.KThread(target=self.__get_meta_data)
        meta_thread.daemon = True
        meta_thread.start()

        # Instantiates the connection with the hls stream
        cap = cv2.VideoCapture(self.hls_url)

        # Make sure thread has finished before starting main loop
        meta_thread.join()

        # Exit thread if stream was not found
        if not self.__found_stream:
            cap.release()
            logging.warning('Stream was not found. Retrying...')
            return False

        # Saves the current time of a successful established connection
        self.__thread_start_time = time.time()

        # Exit because capture did not start correctly
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        if self.fps == 0:
            logging.warning('Capture not found correctly. Retrying...')
            return False

        # How much time has to get awaited between frames
        wait_ms = 1000 / self.fps

        # Reset some variables
        self.__drop_reconnect = False
        self.__reconnecting = False

        # Done with probing, starting the reading thread
        self.__reading_thread = kthread.KThread(target=self.__read, args=(cap, self.__thread_start_time,
                                                                          self.__hls_start_time_stamp, wait_ms,))
        self.__reading_thread.daemon = True
        self.__thread_running = True
        self.__previous_time = time.time()
        self.__reading_thread.start()
        logging.info("Reading thread started successfully!")

        # Start the reconnect thread
        self.__reconnect_thread = kthread.KThread(target=self.reconnect)
        self.__reconnect_thread.daemon = True
        self.__reconnect_thread.start()
        logging.info("Reconnecting thread started successfully!")

        return True

    def reconnect(self):
        """Method to loop and check if we need to reconnect

        """
        while not self.__reconnecting:
            if self.__drop_reconnect:
                logging.info("Shutting down reconnection thread.")
                break
            time.sleep(1)
        else:
            logging.info("Connection lost unexpectedly. Starting connection process")
            if self.__reading_thread.is_alive():
                self.__reading_thread.kill()
            self.__reading_thread.join()
            self.__connect_to_stream()

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

    def __connect_to_stream(self):
        """Method to connect to the stream

        """
        tries_left = 10

        # Sleep is essential so processor has a prepared self.cap
        while tries_left > 0:
            logging.info(f"Attempting to connect. Attempts left: {tries_left}")
            if self.sync():
                break
            time.sleep(1)
            tries_left -= 1

        # Raise error when capture is never created in other thread
        if not self.__found_stream:
            self.__thread_running = False
            logging.error("cv2.VideoCapture probably raised exception")
            raise TimeoutError("HLS Capture never opened")
