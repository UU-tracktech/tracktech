"""Contains information about a single camera object

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""


class StreamOptions:
    """Camera information object.

    Attributes:
        segment_size (str): Seconds in a single video segment
        segment_amount (str): Amount of video segments for the stream
        encoding (str): The encoding to use for the stream
        low (bool): Whether to encode the video to a low quality
        medium (bool): Whether to encode the video to a medium quality
        high (bool): Whether to encode the video to a high quality
    """
    def __init__(self, segment_size, segment_amount, encoding, low, medium, high):
        """Initializes a camara object that holds values

        Args:
            segment_size (str): Seconds in a single video segment
            segment_amount (str): Amount of video segments for the stream
            encoding (str): The encoding to use for the stream
            low (bool): Whether to encode the video to a low quality
            medium (bool): Whether to encode the video to a medium quality
            high (bool): Whether to encode the video to a high quality
        """

        # Seconds in a single video segment
        self.segment_size = segment_size

        # Amount of video segments for the stream
        self.segment_amount = segment_amount

        # The The encoding to use for the stream
        self.encoding = encoding

        # Whether to use various encoding qualities
        self.low = low
        self.medium = medium
        self.high = high
