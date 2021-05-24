"""Main file running the video processing pipeline.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import sys
import logging
import asyncio

import tornado.ioloop
import tornado.web

from processor.utils.config_parser import ConfigParser

from processor.pipeline.process_frames import prepare_stream, process_stream, opencv_display, send_to_orchestrator

from processor.webhosting.websocket_client import WebsocketClient
from processor.webhosting.html_page_handler import HtmlPageHandler
from processor.webhosting.stream_handler import StreamHandler


def create_app(configs, port):
    """Creates a tornado app on a given port

    Args:
        configs (ConfigParser): configurations of the application
        port (int): Port app exposes
    """
    print('*' * 30)
    print('*   open TORNADO stream on   *')
    print(f'*   http://localhost:{port}    *')
    print('*' * 30)

    # Create app and listen to port
    app = tornado.web.Application([
        (r'/(.*\.html)?', HtmlPageHandler, dict(configs=configs)),
        (r'/video_feed', StreamHandler, dict(configs=configs))
    ])
    app.listen(port)


async def deploy(configs, ws_id):
    """Connects to the orchestrator and starts the process_frames loop

    Args:
        configs (ConfigParser): configurations for the prepare stream
        ws_id (str): Id of the camera processor for the orchestrator
    """
    capture, detector, tracker, ws_url = prepare_stream(configs)
    websocket_client = WebsocketClient(ws_url, ws_id)
    await websocket_client.connect()
    # Initiate the stream processing loop, giving the websocket client
    await process_stream(
        capture,
        detector,
        tracker,
        # Function to call when frame is processed
        lambda frame_obj, detected_boxes, tracked_boxes: send_to_orchestrator(websocket_client,
                                                                              frame_obj,
                                                                              detected_boxes,
                                                                              tracked_boxes
                                                                              ),
        websocket_client
    )


def main():
    """Run the main loop, depending on the mode run on localhost, locally with opencv or in swarm

    Tornado uses a custom IOLoop
    Deploy first needs to connect with the orchestrator before it is able to start the asyncio loop
    """
    # Load the config file
    config_parser = ConfigParser('configs.ini')
    configs = config_parser.configs

    # If mode is tornado
    if configs['Main']['mode'].lower() == 'tornado':
        # Create the app and start the ioloop
        port = int(configs['Main']['port'])
        create_app(configs, port)
        tornado.ioloop.IOLoop.current().start()
    # If we want to run it with opencv gui
    elif configs['Main']['mode'].lower() == 'opencv':
        capture, detector, tracker, _ = prepare_stream(configs)
        asyncio.get_event_loop().run_until_complete(
            process_stream(capture, detector, tracker, opencv_display, None)
        )
    # Deploy mode where all is sent to the orchestrator using the websocket url
    elif configs['Main']['mode'].lower() == 'deploy':
        websocket_id = configs['HLS']['url']
        asyncio.get_event_loop().run_until_complete(deploy(configs, websocket_id))
    else:
        raise AttributeError("Mode you try to run in does not exist")


if __name__ == '__main__':
    # Configure the logger
    logging.basicConfig(filename='main.log', filemode='w',
                        format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    # Run the main function
    main()
