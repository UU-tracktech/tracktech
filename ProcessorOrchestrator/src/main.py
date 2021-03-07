from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from tornado.web import RequestHandler
from clientConnection import ClientSocket

define('port', default=8000, help='port to listen on')


def main():
    """Construct and serve the tornado application."""
    app = Application([
        ('/', HelloWorld),
        ('/client', ClientSocket)
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()


class HelloWorld(RequestHandler):
    def get(self):
        self.write("Hello World")


if __name__ == "__main__":
    main()
