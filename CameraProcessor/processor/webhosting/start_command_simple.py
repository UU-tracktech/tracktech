"""Contains StartCommand subclass with only a cutout and object id.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.webhosting.start_command import StartCommand


class StartCommandSimple(StartCommand):
    """Represents a StartCommand with a cutout."""
    def __init__(self, **kwargs):
        """Adds a cutout to expected key set, then calls parent init.

        Args:
            **kwargs (dict): dict of key-value pairs containing the start command message.
        """
        key_set = {"image"}
        super().__init__(*key_set, **kwargs)
