"""Contains Update class which holds an updated feature_map for a tracked object.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class UpdateCommand:
    """UpdateCommand class that updates the tracking dictionary of which object to track."""
    def __init__(self, feature_map, object_id):
        """Constructor for the StopCommand class.

        Args:
            feature_map ([Float]): Array of float representing the feature_map.
            object_id (Int): The ID of the object the feature_map refers to.
        """
        self.feature_map = feature_map
        self.object_id = object_id
