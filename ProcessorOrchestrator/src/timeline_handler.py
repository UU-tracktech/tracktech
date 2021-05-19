"""HTTP handler to serve tracking timeline data

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
from tornado.web import RequestHandler


class TimeLineHandler(RequestHandler):
    """Request handler that handles get request for log file.

    Handler that can be used to handle a get request, it will write the log file, where newlines are replaced
    with html br tags.
    """

    def get(self):
        """Gets log file contents.

        Writes a response containing the contents of the timeline logfile of the specified objectId

        Returns:
            None
        """
        object_id = self.get_argument("objectId", None)
        if object_id is None:
            self.set_status(400, "Missing 'objectId' query parameter")
            self.finish("Missing 'objectId' query parameter")
            return
        file = open(f"tracking_timelines/tracking_logs_{object_id}.txt", "r")
        data = file.read().replace("\n", "")
        # Remove final comma
        data = data[:-1]
        self.write(f'{{"data":[{data}]}}')

    def data_received(self, chunk):
        """Unused method that could handle streamed request data"""
