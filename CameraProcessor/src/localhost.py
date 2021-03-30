import time

import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpserver
import tornado.process
import tornado.template
import tornado.gen
import logging
import cv2
import os
import sys

from src.input.hls_capture import HlsCapture

logging.basicConfig(filename='localhost.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# Tornado example gotten from: https://github.com/wildfios/Tornado-mjpeg-streamer-python
# Combined with: https://github.com/wildfios/Tornado-mjpeg-streamer-python/issues/7
html_page_path = os.path.abspath(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'webpage',
))

capture = HlsCapture()
PORT = 9090


class HtmlPageHandler(tornado.web.RequestHandler):
    def get(self, file_name='index.html'):
        # Check if page exists
        logging.info('getting html page of browser')
        index_page = os.path.join(html_page_path, file_name)
        if os.path.exists(index_page):
            # Render it
            self.render(index_page)
        else:
            # Page not found, generate template
            err_tmpl = tornado.template.Template('<html> Err 404, Page {{ name }} not found</html>')
            err_html = err_tmpl.generate(name=file_name)
            logging.error(f'no index.html found at path {file_name}')
            # Send response
            self.finish(err_html)


class StreamHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        logging.info('set headers')
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary=--jpgboundary')
        self.set_header('Connection', 'close')

        self.served_image_timestamp = time.time()
        my_boundary = '--jpgboundary'
        while capture.opened():
            ret, frame = capture.get_next_frame()
            ret, jpeg = cv2.imencode('.jpg', frame)
            img = jpeg.tobytes()
            # Generating images for mjpeg stream and wraps them into http resp

            interval = 0.1
            if self.served_image_timestamp + interval < time.time():
                self.write(my_boundary)
                self.write('Content-type: image/jpeg\r\n')
                self.write('Content-length: %s\r\n\r\n' % len(img))
                self.write(img)
                self.served_image_timestamp = time.time()

            try:
                self.flush()
            except Exception:
                print('connection lost with client')
                break


def make_app():
    logging.info('creating app')
    # add handlers
    return tornado.web.Application([
        (r'/', HtmlPageHandler),
        (r'/video_feed', StreamHandler)
    ])


# Print to console link to stream
def generate_message():
    print('*' * 30)
    print('*' + ' ' * 28 + '*')
    print(f'*   open TORNADO stream on   *')
    print(f'*   http://localhost:{PORT}    *')
    print('*' + ' ' * 28 + '*')
    print('*' * 30)


if __name__ == '__main__':
    # bind server on 9090 port
    app = make_app()
    app.listen(PORT)
    generate_message()
    tornado.ioloop.IOLoop.current().start()
