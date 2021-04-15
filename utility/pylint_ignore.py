"""Import utils to be able to give proper commands to pylint.

"""
from pylint.utils import utils as pylintutils


class PylintIgnorePaths:
    """Patterns to ignore when linting

    """
    def __init__(self, *paths):
        """Gets paths

        """
        self.paths = paths
        self.original_expand_modules = pylintutils.expand_modules
        pylintutils.expand_modules = self.patched_expand

    def keep_item(self, item):
        """Throws out all ignored file paths and subpaths

        """
        if any(1 for path in self.paths if item['path'].startswith(path)):
            return False

        return True

    def patched_expand(self, *args, **kwargs):
        """Get correct filepaths for linting

        """
        result, errors = self.original_expand_modules(*args, **kwargs)

        result = list(filter(keep_item, result))

        return result, errors
