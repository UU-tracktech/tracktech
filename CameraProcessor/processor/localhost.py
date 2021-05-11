"""File that displays the video stream on a localhost for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import logging
import os
import sys
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpserver
import tornado.process
import tornado.template
import tornado.gen

from processor.stream_handler import StreamHandler

logging.basicConfig(filename='localhost.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# Tornado example gotten from: https://github.com/wildfios/Tornado-mjpeg-streamer-python
# Combined with: https://github.com/wildfios/Tornado-mjpeg-streamer-python/issues/7


class HtmlPageHandler(tornado.web.RequestHandler):
    """Handler for the html page of the site that is for the main page."""
    def get(self, file_name='index.html') -> None:
        """Gets the html page and renders it.

        When the index.html page cannot be found it will send an error template to the webclient.

        Args:
            file_name (str): html page it is getting.
        """
        # Check if page exists
        logging.info('getting html page of browser')
        html_dir_path = os.path.dirname(os.path.realpath(__file__)) + '/../webpage'
        index_page = os.path.join(html_dir_path, file_name)
        if os.path.exists(index_page):
            # Render it
            self.render(index_page)
        else:
            # Page not found, generate template
            err_tmpl = tornado.template.Template('<html> Err 404, Page {{ name }} not found</html>')
            err_html = err_tmpl.generate(name=file_name)
            logging.error(f'no index.html found at path {index_page}')
            # Send response
            self.finish(err_html)


def make_app():
    """Creates the tornado web app.

    Returns:
        tornado.web.Application: Tornado web app with the main page and video handler.
    """
    logging.info('creating app')
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
    main()
