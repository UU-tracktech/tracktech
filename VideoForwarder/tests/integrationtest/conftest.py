"""Contains fixture for the tornado application that mocks the a connection

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import pytest
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    """Tornado web application

    """
    def get(self):
        """Empty get

        """
        self.write("")


@pytest.fixture
def app():
    """Creates application

    Return:
         application: tornado application
    """
    return tornado.web.Application([
        (r"/", MainHandler),
    ])
