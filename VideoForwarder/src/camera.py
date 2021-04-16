<<<<<<< HEAD
# Object to store camera stream information in
class Camera:
    def __init__(self, ip, audio):
        self.ip = ip
        self.conversion = None
        self.callback = None
        self.audio = audio
=======
"""
Contains information about a single camera object
"""


class Camera:
    """
    Camera information object
    """

    def __init__(self, ip, audio):
        self.ip = ip
        """The ip address (with credentials) of the camera"""
    
        self.conversion = None
        """The conversion process creating a hls stream from the camera feed"""
    
        self.callback = None
        """A callback to stop the conversion at a set delay"""

        self.audio = audio
        """Whether the camera stream contains audio"""
>>>>>>> 9f9c67c8b7ba1395dc99b9ef33f6c9182b448f18
