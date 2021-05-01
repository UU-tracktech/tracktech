"""Contains information about a single camera object

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""


class Camera:
    """Camera information object.

    Attributes:
        ip_address (str): Address of the camera
        conversion (str): Conversion used to encode camera
        callback (func): Callback function to stop running after a delay
        audio (bool): Does camera contain audio
    """
    def __init__(self, ip_address, audio):
        """Initializes a camara object that holds values

        Args:
            ip_address (str): Address of the camera
            audio (bool): Whether camera contains audio
        """
        # The ip address (with credentials) of the camera
        self.ip_address = ip_address

        # The conversion process creating a hls stream from the camera feed
        self.conversion = None

        # A callback to stop the conversion at a set delay
        self.callback = None

        # Whether the camera stream contains audio
        self.audio = audio
