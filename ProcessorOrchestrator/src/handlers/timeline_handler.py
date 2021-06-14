"""HTTP handler to serve tracking timeline data.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os

from tornado.web import RequestHandler


class TimelineHandler(RequestHandler):
    """Request handler that handles get request for log file.

    Handler that can be used to handle a get request, it will write the log file, where newlines are replaced
    with html br tags.
    """

    def set_default_headers(self):
        """Sets the default request headers for the request."""
        self.set_header("Access-Control-Allow-Origin", "*")

    def get(self):
        """Gets log file contents.

        Writes a response containing the contents of the timeline logfile of the specified objectId.
        """
        object_id = self.get_argument("objectId", None)
        if object_id is None:
            self.set_status(400, "Missing 'objectId' query parameter")
            self.finish("Missing 'objectId' query parameter")
            return
        filename = f"tracking_timelines/tracking_logs_{object_id}.txt"
        if not os.path.exists(filename):
            self.set_status(400, "Object id not present in tracking history")
            self.finish("Object id not present in tracking history")
            return
        file = open(filename, "r")
        data = file.read().replace("\n", "")
        # Remove final comma.
        data = data[:-1]
        self.write(f'{{"data":[{data}]}}')
        file.close()

    def data_received(self, chunk):
        """Unused method that could handle streamed request data.

        Args:
            chunk (bytes): Byte data received from the server.
        """
