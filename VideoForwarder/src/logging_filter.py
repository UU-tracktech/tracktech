"""A filter that filters specific logs that are produced by the default logger of Tornado.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

from logging import Filter, LogRecord


class LoggingFilter(Filter):
    """The log filter object
    """

    def __init__(self, name="LoggingFilter"):
        """Create a new filter instance

        Args:
            name (str): Name of the filter instance
        """

        # Instantiate a new filter with a given name
        Filter.__init__(self, name)

    def filter(self, record):
        """Filter the log records

        Args:
            record (LogRecord): Contains all the information pertinent to the event being logged

        Returns:
        LogRecord: Log messages that have been filtered
        """

        # Removes logs messages that contains '200 GET'
        return not record.getMessage().startswith("200 GET")
