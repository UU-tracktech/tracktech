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
        if item in self:
            return self[item]
        return None

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        if item in self:
            del self[item]
        else:
            raise AttributeError(f"No entry {item} in Start Command to delete")
