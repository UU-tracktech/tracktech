import os
import tornado.web
import tornado.ioloop

if __name__ == "__main__":
    app = tornado.web.Application([
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': '/streams/'})
    ])

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
