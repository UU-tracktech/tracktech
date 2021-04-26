"""Reads the first environment variables and starts the webserver.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
import json
import ssl
import tornado.httpserver
import tornado.web
import tornado.ioloop

from src.camera import Camera
from src.camera_handler import CameraHandler


def convert_json_to_camera(json_file):
    """Converts json file content to camera objects inside dict

    Args:
        jsonFile: Path to json file which contains cameras

    Returns:
        Dict{Camera_name, Camera_obj}: camera created from json file content in dictionary
    """
    return {camera["Name"]: Camera(camera["Ip"], camera["Audio"]) for camera in json_file}


if __name__ == "__main__":
    print('starting server')

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

    # Get the public key path used for authentication
    public_key_path = os.environ.get('PUBLIC_KEY_PATH')
    print('using auth' if public_key_path is not None else 'not using auth')

    # If the public key path was supplied, read the file and store it
    public_key = None
    if public_key_path:
        public_key_file = open(public_key_path, "r")
        public_key = public_key_file.read()
        public_key_file.close()

    # Create the web application with the camera handler and the public key
    app = tornado.web.Application(
        [
            (r'/(.*)', CameraHandler, {'path': os.environ['STREAM_FOLDER']}),
        ], publicKey=public_key)

    # If using tls, create a context and load the certificate and key in it
    if use_tls:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(cert, key)

        # Start the secure webserver on port 443
        http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)
        http_server.listen(443)
        print('listening on port 443 over https')

    # Else start the insecure webserver on port 80
    else:
        # Start the insecure webserver on port 80
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(80)
        print('listening on port 80 over http')

    # Start the IO loop (used by tornado itself)
    tornado.ioloop.IOLoop.current().start()
