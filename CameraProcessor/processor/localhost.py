"""File that displays the video stream on a localhost for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import logging
import sys
import os
import configparser
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpserver
import tornado.process
import tornado.template
import tornado.gen

from processor.webhosting.html_page_handler import HtmlPageHandler
from processor.webhosting.stream_handler import StreamHandler

# Tornado example gotten from: https://github.com/wildfios/Tornado-mjpeg-streamer-python
# Combined with: https://github.com/wildfios/Tornado-mjpeg-streamer-python/issues/7


def make_app():
    """Creates the tornado web app.

    Returns:
        tornado.web.Application: Tornado web app with the main page and video handler.
    """
    return tornado.web.Application([
        (r'/', HtmlPageHandler),
        (r'/video_feed', StreamHandler)
    ])


def generate_message(port):
    """Generates message to terminal so user can click link.

    Args:
        port (int): port at which localhost page is located.
    """
    print('*' * 30)
    print('*' + ' ' * 28 + '*')
    print('*   open TORNADO stream on   *')
    print(f'*   http://localhost:{port}    *')
    print('*' + ' ' * 28 + '*')
    print('*' * 30)


def main():
    """Creates the tornado app and starts event loop."""
    port = 9090
    app = make_app()
    app.listen(port)
    generate_message(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    # Logging
    logging.basicConfig(filename='localhost.log', filemode='w',
                        format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    main()
