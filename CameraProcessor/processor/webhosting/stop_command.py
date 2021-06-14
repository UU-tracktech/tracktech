"""Contains StopCommand class which holds information about which object should no longer be tracked.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class StopCommand:
    """StopCommand class that stores data regarding which object to stop tracking."""
    def __init__(self, object_id):
        """Constructor for the StopCommand class.

        Args:
            object_id (int): Identifier of the object that should not be tracked any longer.
        """
        self.object_id = object_id
