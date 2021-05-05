"""Starts the tornado webserver.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import sys
import os
import json
import ssl
import tornado.httpserver
import tornado.web
import tornado.ioloop

from auth.auth import Auth
from src.logging_filter import LoggingFilter
from src.camera import Camera
from src.camera_handler import CameraHandler


def convert_json_to_camera(json_file):
    """Converts json file content to camera objects inside dict

    Args:
        jsonFile (str): Path to json file which contains cameras

    Returns:
        Dict{Camera_name, Camera_obj}: camera created from json file content in dictionary
    """
    return {camera["Name"]: Camera(camera["Ip"], camera["Audio"]) for camera in json_file}


# pylint: disable=invalid-name
if __name__ == "__main__":
    # Setup for logging
    tornado.log.logging.basicConfig(filename='/src/main.log', filemode='w',
                                    format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                                    level=tornado.log.logging.INFO,
                                    datefmt='%Y-%m-%d %H:%M:%S')

    tornado.log.gen_log.addHandler(tornado.log.logging.StreamHandler(sys.stdout))
    tornado.log.access_log.addHandler(tornado.log.logging.StreamHandler(sys.stdout))
    tornado.log.access_log.addFilter(LoggingFilter())

    tornado.log.gen_log.info('starting server')

    # Get the config path, read it and parse the json and close it.
    configFile = open(os.environ.get('CONFIG_PATH'), "r")
    configJson = json.loads(configFile.read())
    configFile.close()

    # Process the json config and store the individual cameras
    CameraHandler.cameras = {camera["Name"]: Camera(camera["Ip"], camera["Audio"]) for camera in configJson}

    # Get the ssl certificate and key if supplied, use_tls to indicate both are present
    cert = os.environ.get('SSL_CERT')
    key = os.environ.get('SSL_KEY')
    use_tls = cert and key

    # Get auth ready by reading the environment variables
    public_key, audience = os.environ.get('PUBLIC_KEY'), os.environ.get('AUDIENCE')
    authenticator = None
    if public_key is not None and audience is not None:
        client_role = os.environ.get('CLIENT_ROLE')
        if client_role is not None:
            tornado.log.gen_log.info("using client token validation")
            authenticator = Auth(public_key_path=public_key, algorithms=['RS256'],
                                 audience=audience, role=client_role)

    # Create the web application with the camera handler and the public key
    app = tornado.web.Application(
        [
            (r'/(.*)', CameraHandler, {'path': os.environ['STREAM_FOLDER']}),
        ], authenticator=authenticator)

    # If using tls, create a context and load the certificate and key in it
    if use_tls:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(cert, key)

        # Start the secure webserver on port 443
        http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)
        http_server.listen(443)
        tornado.log.gen_log.info('listening on port 443 over https')

    # Else start the insecure webserver on port 80
    else:
        # Start the insecure webserver on port 80
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(80)
        tornado.log.gen_log.info('listening on port 80 over http')

    # Start the IO loop (used by tornado itself)
    tornado.ioloop.IOLoop.current().start()
