"""Contains StartCommand class which holds information about which object should be tracked.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class StartCommand(dict):
    """StartCommand class that stores data regarding which object to start tracking.

    It uses the dict __init__ to add the **kwargs or dict to this class. This class is, for all intents and purposes,
    a dictionary with entries accessible like properties. Additional functionality can be added.

    We expect some, but not all, of the following key-value pairs:
    - object_id=(int)
    - box_id=(int)
    - frame_id=(int)
    - cutout=(np.ndarray)
    """
    def __getattr__(self, item):
        """Retrieves dict items as properties. Returns None if it is not in the dict, so no errors thrown."""
        if item in self:
            return self[item]
        return None

    def __setattr__(self, key, value):
        """Sets a key to a value, as if setting a property."""
        self[key] = value

    def __delattr__(self, item):
        """Deletes an entry in the dict, as if deleting a property. Raises an error if the item is not in the dict!"""
        if item in self:
            del self[item]
        else:
            raise AttributeError(f"No entry {item} in Start Command to delete")
