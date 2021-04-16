"""entrypoint stuff
1
2
3
"""
import os
import json
import ssl
import tornado.httpserver
import tornado.web
import tornado.ioloop

from camera import Camera
from camera_handler import CameraHandler

if __name__ == "__main__":
    print('starting server')

    # Read the config file
    configFile = open(os.environ.get('CONFIG_PATH'), "r")
    configJson = json.loads(configFile.read())
    configFile.close()

    # Save the cameras in the stat
    CameraHandler.cameras = {camera["Name"]: Camera(camera["Ip"], camera["Audio"]) for camera in configJson}

    # Get ssl ready, if provided in the environment variables
    cert = os.environ.get('SSL_CERT')
    key = os.environ.get('SSL_KEY')
    use_tls = cert is not None and key is not None

    # Read the public key file if applicable
    publicKeyPath = os.environ.get('PUBLIC_KEY_PATH')
    print('using auth' if publicKeyPath is not None else 'not using auth')
    PUBLIC_KEY = None
    if publicKeyPath is not None:
        publicKeyFile = open(publicKeyPath, "r")
        publicKey = publicKeyFile.read()
        publicKeyFile.close()

    # Create a web application
    app = tornado.web.Application(
        [
            (r'/(.*)', CameraHandler, {'path': os.environ['STREAM_FOLDER']}),
        ], publicKey = publicKey) #store the public key

    if use_tls:
        # Create a ssl context
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(cert, key)

        # Create a http server, with optional ssl.
        http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)
        http_server.listen(443)
        print('listening on port 443 over https')

    else:
        # Create a http server, with optional ssl.
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(80)
        print('listening on port 80 over http')

    # Start io loop
    tornado.ioloop.IOLoop.current().start()
