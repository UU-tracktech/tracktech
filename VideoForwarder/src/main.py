<<<<<<< HEAD
"""entrypoint stuff
1
2
3
"""
import os
import tornado.httpserver
import tornado.web
import tornado.ioloop
import json
import ssl

from camera import Camera
from cameraHandler import CameraHandler
=======
"""
Reads the first environment variables and starts the webserver.
"""
import os
import json
import ssl
import tornado.httpserver
import tornado.web
import tornado.ioloop

from camera import Camera
from camera_handler import CameraHandler
>>>>>>> 9f9c67c8b7ba1395dc99b9ef33f6c9182b448f18

if __name__ == "__main__":
    print('starting server')

<<<<<<< HEAD
    # Read the config file
=======
>>>>>>> 9f9c67c8b7ba1395dc99b9ef33f6c9182b448f18
    configFile = open(os.environ.get('CONFIG_PATH'), "r")
    configJson = json.loads(configFile.read())
    configFile.close()
    """Get the config path, read it and parse the json and close it."""

<<<<<<< HEAD
    # Save the cameras in the stat
    CameraHandler.cameras = {camera["Name"]: Camera(camera["Ip"], camera["Audio"]) for camera in configJson}
=======
    CameraHandler.cameras = {camera["Name"]: camera(camera["Ip"], camera["Audio"]) for camera in configJson}
    """Process the json config and store the individual cameras"""
>>>>>>> 9f9c67c8b7ba1395dc99b9ef33f6c9182b448f18

    cert = os.environ.get('SSL_CERT')
    key = os.environ.get('SSL_KEY')
    use_tls = cert is not None and key is not None
    """Get the ssl certificate and key if supplied, use_tls to indicate both are present"""

    publicKeyPath = os.environ.get('PUBLIC_KEY_PATH')
    print('using auth' if publicKeyPath is not None else 'not using auth')
    """Get the public key path used for authentication"""

    publicKey = None
    if publicKeyPath is not None:
        publicKeyFile = open(publicKeyPath, "r")
        publicKey = publicKeyFile.read()
        publicKeyFile.close()
    """If the public key path was supplied, read the file and store it"""

<<<<<<< HEAD
    # Read the public key file if applicable
    publicKeyPath = os.environ.get('PUBLIC_KEY_PATH')
    print('using auth' if publicKeyPath is not None else 'not using auth')
    publicKey = None
    if publicKeyPath is not None:
        publicKeyFile = open(publicKeyPath, "r")
        publicKey = publicKeyFile.read()
        publicKeyFile.close()

    # Create a web application
    app = tornado.web.Application(
        [
            (r'/(.*)', CameraHandler, {'path': 'streams'}),
        ], publicKey = publicKey) #store the public key
=======
    app = tornado.web.Application(
        [
            (r'/(.*)', CameraHandler, {'path': os.environ['STREAM_FOLDER']}),
        ], publicKey = publicKey)
    """Create the web application with the camera handler and the public key"""
>>>>>>> 9f9c67c8b7ba1395dc99b9ef33f6c9182b448f18

    if use_tls:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(cert, key)
        """If using tls, create a context and load the certificate and key in it"""

        http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)
        http_server.listen(443)
        print('listening on port 443 over https')
        """Start the secure webserver on port 443"""

    else:
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(80)
        print('listening on port 80 over http')
        """Start the insecure webserver on port 80"""

    tornado.ioloop.IOLoop.current().start()
    """Start the IO loop (used by tornado itself)"""
