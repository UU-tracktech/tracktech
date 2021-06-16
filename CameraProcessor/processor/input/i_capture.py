"""Contains the ICapture interface for different capture methods.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class ICapture:
    """Superclass for a capture without implemented methods to enforce the definition of them."""
    def opened(self):
        """Returns whether the capture object still opened.

        Returns:
            bool: Boolean, which indicates whether stream is still opened
        """
        raise NotImplementedError('stopped method not implemented')

    def close(self):
        """Closes capture object, which prevents getting more frames."""
        raise NotImplementedError('No close defined for the capture')

    def get_next_frame(self):
        """Gets the next frame from the capture.

        Returns:
            bool, FrameObj: Boolean whether a next frame was found.
                            Frame from the capture object.
        """
        raise NotImplementedError('No implementation for getting next frame')
