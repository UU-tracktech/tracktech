"""HTTP handler to return an array of tracked object ids.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from tornado.web import RequestHandler

from src.objects.object_management import objectHistory


class ObjectIdsHandler(RequestHandler):
    """Request handler that handles get request for object ids.

    Handler that can be used to handle a get request, return an array of object ids that have been tracked.
    """

    def set_default_headers(self):
        """Sets the default request headers for the request."""
        self.set_header("Access-Control-Allow-Origin", "*")

    def get(self):
        """Gets object ids.

        Writes a response containing an array of object ids.
        """
        self.write(f'{{"data":{objectHistory}}}')

    def data_received(self, chunk):
        """Unused method that could handle streamed request data.

        Args:
            chunk (Union[str, bytes, dict]): Chunk received from the server.
        """
