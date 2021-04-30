"""Contains the ICapture interface for different capture methods

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

from typing import List


class ICapture:
    """Superclass for a capture without implemented methods to enforce the definition of them."""
    def opened(self):
        """Returns whether the capture object still opened.

        Returns:
            Boolean which indicates whether stream is still opened
        """
        raise NotImplementedError('stopped method not implemented')

    def close(self) -> None:
        """Closes capture object which prevents getting more frames
        """
        raise NotImplementedError('No close defined for the capture')

    def get_next_frame(self) -> (bool, List[List[int]]):
        """Gets the next frame from the capture

        Returns:
            Boolean whether a next frame was found
            Frame from the capture object
        """
        raise NotImplementedError('No implementation for getting next frame')

    def get_capture_length(self) -> int:
        """Returns the length of the video, image directory, or if its a stream,
        None

        Returns:
            An integer describing the length
        """
        raise NotImplementedError("No implementation for get_vid_length")
