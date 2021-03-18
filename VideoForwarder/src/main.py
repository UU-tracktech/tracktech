import os
import tornado.web
import tornado.ioloop
from subprocess import Popen

class fileHandler(tornado.web.StaticFileHandler):
    def get_absolute_path(self, root, path):

        abspath = os.path.abspath(os.path.join(root, path))
        if not os.path.exists(abspath):
            Popen(['ffmpeg','-rtsp_transport','tcp','-i','rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov','-r','100','-crf','25','-preset','faster','-maxrate','500k','-bufsize','1500k','-c:v','libx264','-hls_time','10','-hls_list_size','2','-hls_wrap','2','-start_number','1','-rtsp_transport','tcp',abspath])      
        return abspath

if __name__ == "__main__":
    app = tornado.web.Application([ 
        (r"/(.*)", fileHandler, {'path': 'streams'})
    ])
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()