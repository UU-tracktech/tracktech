"""Contains the ICapture interface for different capture methods

"""

from typing import List


class ICapture:
    """Superclass for a capture without implemented methods to enforce the definition of them

    """
    def opened(self) -> bool:
        """Returns whether the capture object still opened

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
