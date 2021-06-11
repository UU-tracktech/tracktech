"""HTTP server setup.

This file contains methods to create a http or https server.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import os
import ssl

from tornado.httpserver import HTTPServer

import src.logger as logger


def create_http_servers(app):
    """Creates http server and https server if ssl options are given in the environment.

    Args:
        app (tornado.web.Application): the web application to use when creating the servers.

    Returns:
        HTTPServer, HTTPServer: The one or two created tornado http servers, second one containing ssl options.
    """
    # Get ssl ready, if provided in the environment variables.
    cert = os.environ.get('SSL_CERT')
    key = os.environ.get('SSL_KEY')

    https_server = None

    if cert is not None and key is not None:
        # Create a ssl context.
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(cert, key)

        # Create a http server, with optional ssl.
        https_server = HTTPServer(app, ssl_options=ssl_ctx)
        https_server.listen(443)
        logger.log('listening over https')

    # Create a http server.
    http_server = HTTPServer(app)
    http_server.listen(80)
    logger.log('listening over http')

    return http_server, https_server
