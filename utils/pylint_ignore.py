"""Import utils to be able to give proper commands to pylint. Pylint default functionality is broken;
it is not ignoring folders that are added to the ignore= part of the .pylintrc.
Therefore we had to override the file .py filesselection.

"""
from pylint.utils import utils as pylint_utils


class PylintIgnorePaths:
    """Patterns to ignore when linting

    """
    def __init__(self, *paths):
        """Gets paths

        """
        self.paths = paths
        self.original_expand_modules = pylint_utils.expand_modules
        pylint_utils.expand_modules = self.patched_expand

    def patched_expand(self, *args, **kwargs):
        """Get correct filepaths for linting

        """
        result, errors = self.original_expand_modules(*args, **kwargs)

        def keep_item(item):
            """Throws out all ignored file paths and subpaths

            """
            if any(1 for path in self.paths if item['path'].startswith(path)):
                return False

            return True

        result = list(filter(keep_item, result))

        return result, errors
