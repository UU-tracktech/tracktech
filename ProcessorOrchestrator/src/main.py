from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from client import ClientSocket
from processor import ProcessorSocket
from logger import LogHandler
define('port', default=8000, help='port to listen on')


def main():
    # Define socket for both client and processor
    handlers = [
        ('/client', ClientSocket),
        ('/processor', ProcessorSocket),
        ('/logs', LogHandler)
    ]

    # Construct and serve the tornado application.
    app = Application(handlers)

    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on port %i' % options.port)
    IOLoop.current().start()


if __name__ == "__main__":
    main()
