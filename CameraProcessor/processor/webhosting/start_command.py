"""Contains StartCommand class which holds information about which object should be tracked.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class StartCommand:
    """StartCommand class that stores data regarding which object to start tracking."""
    def __init__(self, frame_id, box_id, object_id):
        """Constructor for the StartCommand class.

        Args:
            frame_id (timestamp): Id of the frame which contains the object to be tracked.
            box_id (int): Id of the box that contains the object to be tracked.
            object_id (int): Identifier to track the object with   .
        """
        self.frame_id = frame_id
        self.box_id = box_id
        self.object_id = object_id
