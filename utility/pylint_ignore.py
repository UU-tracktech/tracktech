"""Import utils to be able to give proper commands to pylint.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from pylint.utils import utils as pylintutils


class PylintIgnorePaths:
    """Patterns to ignore when linting."""
    def __init__(self, *paths):
        """Gets paths."""
        self.paths = paths
        self.original_expand_modules = pylintutils.expand_modules
        pylintutils.expand_modules = self.patched_expand

    def patched_expand(self, *args, **kwargs):
        """Get correct file paths for linting."""
        result, errors = self.original_expand_modules(*args, **kwargs)

        # Filter on paths.
        result = list(filter(lambda item: not any(1 for path in self.paths if item['path'].startswith(path)), result))

        # Ignore __init__.py files.
        result = [item for item in result if not item['path'].endswith('__init__.py')]

        return result, errors
