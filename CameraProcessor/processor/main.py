"""Main file running the video processing pipeline.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import sys
import logging
import os
import asyncio
import configparser
import cv2

import tornado.ioloop
import tornado.web

import processor.utils.text as text
import processor.utils.draw as draw

from processor.pipeline.process_frames import prepare_stream, process_stream
import processor.webhosting.websocket_client as client

from processor.webhosting.html_page_handler import HtmlPageHandler
from processor.webhosting.stream_handler import StreamHandler


async def __send_orchestrator(ws_client, frame_obj, tracked_boxes):
    """Sends the bounding boxes to the orchestrator using a websocket client

    Args:
        frame_obj (FrameObj): Frame object on which drawing takes place
        tracked_boxes (BoundingBoxes):
    """
    # Get message and send it through the websocket
    client_message = text.bounding_boxes_to_json(tracked_boxes, frame_obj.get_timestamp())
    ws_client.write_message(client_message)
    logging.info(client_message)

    # Give control to asyncio to work through queue
    await asyncio.sleep(0)


async def __opencv_display(frame_obj, tracked_boxes):
    """Displays frame using the cv2.imshow

    Is async because the process_frames.py loop expects to get a async function it can await

    Args:
        frame_obj (FrameObj): Frame object on which drawing takes place
        tracked_boxes (BoundingBoxes):
    """
    # Copy frame to draw over.
    frame_copy = frame_obj.get_frame().copy()

    # Draw bounding boxes with ID
    draw.draw_tracking_boxes(frame_copy, tracked_boxes.get_bounding_boxes())

    # Play the video in a window called "Output Video"
    try:
        cv2.imshow("Output Video", frame_copy)
    except OSError as err:
        # Figure out how to get Docker to use GUI
        raise OSError("Error displaying video. Are you running this in Docker perhaps?") \
            from err

    # This next line is **ESSENTIAL** for the video to actually play
    # A timeout of 0 will not display the image
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()


async def deploy(ws_id):
    """Connects to the orchestrator and starts the process_frames loop

    Args:
        ws_id (str): Id of the camera processor for the orchestrator
    """
    capture, detector, tracker, ws_url = prepare_stream()
    ws_client = await client.create_client(ws_url, ws_id)
    # Initiate the stream processing loop
    await process_stream(
        capture,
        detector,
        tracker,
        # Function to call when frame is processed
        lambda frame_obj, bounding_boxes: __send_orchestrator(ws_client, frame_obj, bounding_boxes)
    )


def main():
    """Run the main loop, depending on the mode run on localhost, locally with opencv or in swarm

    Tornado uses a custom IOLoop
    Deploy first needs to connect with the orchestrator before it is able to start the asyncio loop
    """
    # Load the config file
    configs = configparser.ConfigParser(allow_no_value=True)
    __root_dir = os.path.join(os.path.dirname(__file__), '../')
    configs.read(os.path.realpath(os.path.join(__root_dir, 'configs.ini')))

    # If mode is tornado
    if configs['Main']['mode'].lower() == 'tornado':
        # Create the app
        port = int(configs['Main']['port'])
        print('*' * 30)
        print(f'*   open TORNADO stream on   *')
        print(f'*   http://localhost:{port}    *')
        print('*' * 30)
        app = tornado.web.Application([
            (r'/', HtmlPageHandler),
            (r'/video_feed', StreamHandler)
        ])
        # Listen to port
        app.listen(port)
        # Start httpserver
        tornado.ioloop.IOLoop.current().start()
    # If we want to run it with opencv gui
    elif configs['Main']['mode'].lower() == 'opencv':
        capture, detector, tracker, url = prepare_stream()
        asyncio.get_event_loop().run_until_complete(
            process_stream(capture, detector, tracker, __opencv_display)
        )
    # Deploy mode where all is sent to the orchestrator using the websocket url
    elif configs['Main']['mode'].lower() == 'deploy':
        websocket_id = configs['HLS']['url']
        asyncio.get_event_loop().run_until_complete(deploy(websocket_id))
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
    try:
        main()
    # Yolov5 throws a general SystemExit
    except SystemExit:
        pass
