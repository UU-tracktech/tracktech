"""Reads out environment variables to determine how the camera stream should be run.
Chosen for environment variables since these are supported on any OS and work very similar

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os


def get_stream_variables():
    """Gets stream variables from the environment with default values

    Returns (str, str, str, str, str):
        Size of the segment
        The maximum number of segments stored
        Encoding method used to encode the stream
        Timeout before stream stops running
        After stopping the stream the files will exist this long
    """
    # How long each video segment should be in seconds
    segment_size = os.environ.get('SEGMENT_SIZE') or '2'

    # How many segments of a video stream should be stored at once at a given time
    segment_amount = os.environ.get('SEGMENT_AMOUNT') or '5'

    # The FFMPEG encoding that should be used to encode the video streams
    encoding = os.environ.get('ENCODING') or 'libx264'

    # How long the stream has no requests before stopping the conversion in seconds
    remove_delay = float(os.environ.get('REMOVE_DELAY') or '60.0')

    # The maximum amount of seconds we will wait with removing stream files after stopping the conversion
    timeout_delay = int(os.environ.get('TIMEOUT_DELAY') or '30')

    return segment_size, segment_amount, encoding, remove_delay, timeout_delay
