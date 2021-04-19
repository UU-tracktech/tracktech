"""File that displays the video stream on a localhost for testing.

"""

import time
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
import cv2

from processor.input.hls_capture import HlsCapture

logging.basicConfig(filename='localhost.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# Tornado example gotten from: https://github.com/wildfios/Tornado-mjpeg-streamer-python
# Combined with: https://github.com/wildfios/Tornado-mjpeg-streamer-python/issues/7


class HtmlPageHandler(tornado.web.RequestHandler):
    """Handler for the html page of the site that is for the main page

    """
    def get(self, file_name='index.html') -> None:
        """Gets the html page and renders it

        When the index.html page cannot be found it will send an error template to the webclient

        Args:
            file_name (str): html page it is getting

        """
        # Check if page exists
        logging.info('getting html page of browser')
        html_dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\..\\webpage'
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


class StreamHandler(tornado.web.RequestHandler):
    """Handler for the frame stream

    """
    server_image_timestamp = 0

    @tornado.gen.coroutine
    def get(self):
        """ Get request handler for the webpage to show video stream.

        """
        # Sets headers of the handler
        logging.info('set headers')
        self.set_header('Cache-Control',
                        'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary=--jpgboundary')
        self.set_header('Connection', 'close')

        served_image_timestamp = time.time()
        my_boundary = '--jpgboundary'

        # Create capture and start read loop
        capture = HlsCapture()
        while capture.opened():
            # Get frame
            ret, frame, _ = capture.get_next_frame()
            if not ret:
                continue
            # If it does get the image the frame gets encoded
            ret, jpeg = cv2.imencode('.jpg', frame)
            img = jpeg.tobytes()

            # Every .1 seconds the frame gets sent to the browser
            interval = 0.1
            if served_image_timestamp + interval < time.time():
                self.write(my_boundary)
                self.write('Content-type: image/jpeg\r\n')
                self.write('Content-length: %s\r\n\r\n' % len(img))
                self.write(img)
                served_image_timestamp = time.time()

            try:
                self.flush()
            except Exception as err:
                raise Exception('connection lost with client') from err


def make_app() -> tornado.web.Application:
    """Creates the tornado web app

    Returns:
        Tornado web app with the main page and video handler
    """
    logging.info('creating app')
    return tornado.web.Application([
        (r'/', HtmlPageHandler),
        (r'/video_feed', StreamHandler)
    ])


def generate_message(port) -> None:
    """Generates message to terminal so user can click link
    """
    print('*' * 30)
    print('*' + ' ' * 28 + '*')
    print('*   open TORNADO stream on   *')
    print(f'*   http://localhost:{port}    *')
    print('*' + ' ' * 28 + '*')
    print('*' * 30)


if __name__ == '__main__':
    PORT = 9090
    app = make_app()
    app.listen(PORT)
    generate_message(PORT)
    tornado.ioloop.IOLoop.current().start()
