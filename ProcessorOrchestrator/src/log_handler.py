"""HTTP handler to serve the logs

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
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

        Returns:
            None
        """
        file = open("logs.log", "r")
        self.write(file.read().replace("\n", "<br/>"))

    def data_received(self, chunk):
        """Unused method that could handle streamed request data"""
