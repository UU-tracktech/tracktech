"""Main file running the video processing pipeline.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import os
import sys
import logging
import asyncio

import tornado.ioloop
import tornado.web

from processor.utils.config_parser import ConfigParser

from processor.pipeline.prepare_pipeline import prepare_objects
from processor.pipeline.process_frames import process_stream, opencv_display, send_boxes_to_orchestrator

from processor.webhosting.websocket_client import WebsocketClient
from processor.webhosting.html_page_handler import HtmlPageHandler
from processor.webhosting.stream_handler import StreamHandler


def create_app(configs, port):
    """Creates a tornado app on a given port.

    Args:
        configs (ConfigParser): configurations of the application.
        port (int): Port app exposes.
    """
    print('*' * 30)
    print('*   open TORNADO stream on   *')
    print(f'*   http://localhost:{port}    *')
    print('*' * 30)

    # Create app and listen to port.
    app = tornado.web.Application([
        (r'/(.*\.html)?', HtmlPageHandler, dict(configs=configs)),
        (r'/video_feed', StreamHandler, dict(configs=configs))
    ])
    app.listen(port)


def enforce_deploy_environment_variables():
    """Makes sure the environment variables are set correctly when running in deploy mode.

    Returns:
        str, str, str: Id of the camera processor for the orchestrator.
                       URL of the orchestrator WebSocket.
                       URL of the forwarder stream.
    """
    if os.getenv('ORCHESTRATOR_URL') is None or os.getenv('HLS_STREAM_URL') is None or os.getenv('CAMERA_ID') is None:
        raise EnvironmentError('Environment variable CAMERA_ID, HLS_STREAM_URL or ORCHESTRATOR_URL'
                               ' is missing but is required during deployment.')

    # Give back the values found in the environment.
    return os.getenv('CAMERA_ID'), os.getenv('ORCHESTRATOR_URL'), os.getenv('HLS_STREAM_URL')


async def deploy(configs, websocket_id, websocket_url, hls_url):
    """Connects to the orchestrator and starts the process_frames loop

    Args:
        configs (configparser.ConfigParser): configurations for the prepared stream.
        websocket_id (str): Id of the camera processor for the orchestrator.
        websocket_url (str): Url of the orchestrator websocket.
        hls_url (str): Url of the forwarder stream.
    """
    # To deploy, websocket url and forwarder url have to be set in the configurations.
    configs['Input']['type'] = 'hls'
    configs['Input']['hls_url'] = hls_url
    configs['Orchestrator']['url'] = websocket_url

    # Open the capture in combination with the stages and create the client.
    capture, detector, tracker, re_identifier, websocket_url = prepare_objects(configs)
    websocket_client = WebsocketClient(websocket_url, websocket_id)
    await websocket_client.connect()
    # Initiate the stream processing loop, giving the websocket client.
    await process_stream(
        capture,
        detector,
        tracker,
        re_identifier,
        # Function to call when frame is processed.
        lambda frame_obj, detected_boxes, tracked_boxes, re_id_tracked_boxes: send_boxes_to_orchestrator(
                                                                                    websocket_client,
                                                                                    frame_obj,
                                                                                    detected_boxes,
                                                                                    tracked_boxes,
                                                                                    re_id_tracked_boxes
                                                                                    ),
        websocket_client
    )


def main():
    """Run the main loop, depending on the mode run on localhost, locally with opencv or in the swarm.

    Tornado uses a custom IOLoop.
    Deploy first needs to connect with the orchestrator before it is able to start the asyncio loop.

    Raises:
        AttributeError: Mode in which is run does not exist.
        EnvironmentError: CAMERA_ID is missing, but the application is running in deploy mode.
    """
    # Load the config file.
    config_parser = ConfigParser('configs.ini', True)
    configs = config_parser.configs

    # If mode is tornado.
    if configs['Main']['mode'].lower() == 'tornado':
        # Create the app and start the ioloop.
        port = int(configs['Main']['port'])
        create_app(configs, port)
        tornado.ioloop.IOLoop.current().start()
    # If we want to run it with opencv gui.
    elif configs['Main']['mode'].lower() == 'opencv':
        capture, detector, tracker, re_identifier, _ = prepare_objects(configs)
        asyncio.get_event_loop().run_until_complete(
            process_stream(capture, detector, tracker, re_identifier, opencv_display, None)
        )
    # Deploy mode where all is sent to the orchestrator using the websocket URL.
    elif configs['Main']['mode'].lower() == 'deploy':
        # Make environment variables are set when running in deploy.
        ws_id, ws_url, hls_url = enforce_deploy_environment_variables()
        asyncio.get_event_loop().run_until_complete(deploy(configs, ws_id, ws_url, hls_url))
    else:
        raise AttributeError('Mode you try to run in does not exist, did you make a typo?')


if __name__ == '__main__':
    # Configure the logger.
    logging.basicConfig(filename='main.log', filemode='w',
                        format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    # Run the main function.
    main()
