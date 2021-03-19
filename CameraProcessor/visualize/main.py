import tornado.ioloop
import tornado.web
from tornado.options import define, options
import threading
import datetime
import cv2 as cv

define("port", default=8000, help="Listening Port", type=int)
define("url", default=r"http://81.83.10.9:8001/mjpg/video.mjpg", help="Url of HLS Stream", type=str)

outputFrame = None
cap = cv.VideoCapture(options.url)
lock = threading.Lock()

class MainHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.write("Hello, world")

class DetectionHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        img = generate()
        self.write(img)

def readStream():
    global outputFrame,cap

    print("hello")
    if not cap.isOpened:
        print("Can't open stream")

    while True:
        ret, frame = cap.read()
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imwrite('frame.jpg', frame)
        timestamp = datetime.datetime.now()
        cv.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M %S %p"
        ), (10, frame.shape[0] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        with lock:
            outputFrame = frame.copy()

def generate() :
    global outputFrame, lock

    while True:
        with lock:
            if outputFrame is None:
                continue

            (flag, encodedImage) = cv.imencode(".jpg", outputFrame)

            if not flag:
                continue

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/video", DetectionHandler),
    ])

    t = threading.Thread(target=readStream)
    t.daemon = True
    t.start()

    print("We got here")

    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

    print("we got here")

cap.release()