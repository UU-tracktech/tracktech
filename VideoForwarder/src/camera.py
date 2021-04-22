"""Contains information about a single camera object

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""


class Camera:
    """
    Camera information object
    """

    def __init__(self, ip_adress, audio):
        self.ip_adress = ip_adress
        """The ip address (with credentials) of the camera"""

        self.conversion = None
        """The conversion process creating a hls stream from the camera feed"""

        self.callback = None
        """A callback to stop the conversion at a set delay"""

        self.audio = audio
        """Whether the camera stream contains audio"""
