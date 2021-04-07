"""HTTP handler to serve the logs"""
from typing import Optional, Awaitable
from tornado.web import RequestHandler


class LogHandler(RequestHandler):
    """Request handler that handles get request for log file.

    Handler that can be used to handle a get request, it will write the log file, where newlines are replaced
    with html br tags.
    """

    def get(self):
        """Gets log file contents.

        Writes a response containing the contents of the logfile, with html br tags instead of newlines, to increase
        readability.
        """
        file = open("logs.log", "r")
        self.write(file.read().replace("\n", "<br/>"))

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        """Unused method that could handle streamed request data"""
