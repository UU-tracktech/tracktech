import time

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.process
import tornado.template
import tornado.gen
import cv2
import os

from input.hls_stream import HLSCapture

# Tornado example gotten from: https://github.com/wildfios/Tornado-mjpeg-streamer-python
# Combined with: https://github.com/wildfios/Tornado-mjpeg-streamer-python/issues/7
html_page_path = dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\webpage'
capture = HLSCapture()
frame_nr = 0


class HtmlPageHandler(tornado.web.RequestHandler):
    def get(self, file_name='index.html'):
        # Check if page exists
        index_page = os.path.join(html_page_path, file_name)
        if os.path.exists(index_page):
            # Render it
            self.render(index_page)
        else:
            # Page not found, generate template
            err_tmpl = tornado.template.Template('<html> Err 404, Page {{ name }} not found</html>')
            err_html = err_tmpl.generate(name=file_name)
            # Send response
            self.finish(err_html)


class StreamHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary=--jpgboundary')
        self.set_header('Connection', 'close')

        self.served_image_timestamp = time.time()
        my_boundary = '--jpgboundary'
        while True:
            frame = capture.get_next_frame()
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
                yield self.flush()
            else:
                yield self.flush()


def make_app():
    # add handlers
    return tornado.web.Application([
        (r'/', HtmlPageHandler),
        (r'/video_feed', StreamHandler)
    ])


if __name__ == '__main__':
    # bind server on 9090 port
    app = make_app()
    app.listen(9090)
    tornado.ioloop.IOLoop.current().start()
