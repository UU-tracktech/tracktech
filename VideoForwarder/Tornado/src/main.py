import os
import tornado.web
import tornado.ioloop

class fileHandler(tornado.web.StaticFileHandler):
    def get_absolute_path(self, root, path):
        abspath = os.path.abspath(os.path.join(root, path))
        if not os.path.exists(abspath):
            print("not found")
            #Create the file using ffmpeg
        return abspath

if __name__ == "__main__":
    app = tornado.web.Application([ 
        (r"/(.*)", fileHandler, {'path': '/streams/'})
    ])

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
