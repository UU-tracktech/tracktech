# from https://www.tornadoweb.org/en/stable/index.html#
import tornado.ioloop
import tornado.web
import cv2 as cv 
import tensorflow as tf
import sys

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        message = f"Hello, world. \n Python Version: {sys.version}\n OpenCV Version: {cv.__version__}\n Tensorflow Version: {tf.__version__}"
        self.write(message)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()