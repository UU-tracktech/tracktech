"""Contains StartCommand class which holds information about which object should be tracked.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class StartCommand(dict):
    """StartCommand class that stores data regarding which object to start tracking.

    It uses the dict __init__ to add the **kwargs or dict to this class. This class is, for all intents and purposes,
    a dictionary with entries accessible like properties. Additional functionality can be added.
    """
    def __init__(self, *args, **kwargs):
        # Pylint is freaking out about *args for some reason.
        # TODO: fix bug: pylint throws unknown-argument-in-docstring error about *args #pylint: disable=fixme.
        # pylint: disable=unknown-argument-in-docstring
        """Checks if we have an object id, then calls dict init.

        Args:
            *args (set): A set of keys expected in the command.
            **kwargs (dict): dict of key-value pairs containing the start command message.
        """
        # pylint: enable=unknown-argument-in-docstring
        # Add expected keywords to key_set.
        key_set = {"objectId"}
        key_set.update(args)

        # Test if kwargs contains ONLY keys we expect.
        diff = kwargs.keys() - key_set
        if len(diff) > 0:
            raise KeyError(f"Unexpected keyword or keywords {diff} in start command.")

        # Test if kwargs contains ALL the keys we expect.
        diff2 = key_set - kwargs.keys()
        if len(diff2) > 0:
            raise KeyError(f"Missing expected keyword or keywords {diff2} in start command.")
        super().__init__(**kwargs)

    # pylint: disable=docstring-is-missing
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
    # pylint: enable=docstring-is-missing
