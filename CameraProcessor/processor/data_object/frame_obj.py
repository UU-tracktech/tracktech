"""Contains FrameObj class which holds information.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class FrameObj:
    """Frame object contains the frame and corresponding timestamp."""

    def __init__(self, frame, timestamp):
        """Inits the FrameObj with frame and timestamp.

        Args:
            frame (numpy.ndarray): the frame from the capture given by OpenCV.
            timestamp (float): timestamp (in s) associated with the current frame.
        """
        self.__frame = frame
        self.__timestamp = timestamp

    @property
    def frame(self):
        """Gets the frame.

        Returns:
            numpy.ndarray: the frame given when creating the object.
        """
        return self.__frame

    @property
    def timestamp(self):
        """Gets the timestamp (in s) associated with the current frame.

        Returns:
            float: timestamp (in s) of the frame.
        """
        return self.__timestamp

    @property
    def shape(self):
        """Gets shape of frame.

        Returns:
            float, float: (width, height) of frame.
        """
        return self.__frame.shape[1], self.__frame.shape[0]

    def __repr__(self):
        """Converts the frame to a string.

        Returns:
            str: String representation of a frame.
        """
        return f'FrameObj(width:{self.shape[0]} height:{self.shape[1]} timestamp:{self.timestamp:.3f})'
