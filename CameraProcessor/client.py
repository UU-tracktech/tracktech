import asyncio
import json
import sys
import logging
from tornado import websocket
from detection.dectection_obj import DetectionObj
from input.hls_stream import HlsCapture
import cv2
from datetime import datetime
import random

# Setup (basic) logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='file.log',
                    level=logging.INFO,
                    filemode='w')

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

frame_nr = 0
feature_map_delay = 10
capture = HlsCapture()


# Url of websocket server
#url = 'ws://localhost:80/processor'
url = 'wss://tracktech.ml:50010/processor'

# Connection variables
connected = False  # Whether or not the connection is live
connection = None  # Holds the connection object
connect_task_created = False  # Whether or not already trying to reconnect


# Mock methods on received commands
def update_feature_map(message):
    object_id = message["objectId"]
    feature_map = message["featureMap"]
    logging.info(f"Updating object {object_id} with feature map {feature_map}")


def start_tracking(message):
    object_id = message["objectId"]
    frame_id = message["frameId"]
    box_id = message["boxId"]
    logging.info(f"Start tracking box {box_id} in frame_id {frame_id} with new object id {object_id}")


def stop_tracking(message):
    object_id = message["objectId"]
    logging.info(f"Stop tracking object {object_id}")


# Message handler
def read_msg(message):
    if not message:
        logging.error("The websocket connection was closed")
        return
    try:
        message_object = json.loads(message)

        # Switch on message type
        actions = {
            "featureMap":
                lambda: update_feature_map(message_object),
            "start":
                lambda: start_tracking(message_object),
            "stop":
                lambda: stop_tracking(message_object)
        }

        # Execute correct function
        function = actions.get(message_object["type"])
        if function is None:
            logging.warning(f"Someone gave an unknown command: {message}")
        else:
            function()

    except ValueError:
        logging.warning(f"Someone wrote bad json: {message}")
    except KeyError:
        logging.warning(f"Someone missed a property in their json: {message}")


# Write messages to the connection
async def write_message(msg):
    global connection, connected
    try:
        await connection.write_message(msg)

    except websocket.WebSocketClosedError:
        connected = False


# Connect to the specified websocket url
async def connect_to_url():
    global connection, connected, connect_task_created

    while not connected:
        try:
            connection = await websocket.websocket_connect(url, on_message_callback=read_msg)
            logging.info(f"Connected to {url} successfully")
            connected = True
            connect_task_created = False

        except ConnectionRefusedError:
            logging.warning(f"Could not connect to {url}, trying again in 1 second...")
            await asyncio.sleep(1)

def mock_detection_object(frm):
    obj = DetectionObj(datetime.now(), frm, frame_nr)
    obj.bounding_box = obj.mock_bounding_boxes()
    return obj


mock_feature_map_dict = {
    "type": "featureMaps"
}

# Update one of the mock feature maps in the mock dictionary
def update_feature_maps():
    object_id = random.randint(1,10)

    # if key does not yet exist
    if not object_id in mock_feature_map_dict:

        # Create a mock feature map for the object
        mock_feature_map_dict[object_id] = { "state": 0}

    mock_feature_map_dict[object_id]["state"] = mock_feature_map_dict[object_id]["state"] + 1

async def main():
    global connection, connected, connect_task_created, frame_nr

    # Try to get an initial connection
    await connect_to_url()

    # Video processing loop
    while not capture.stopped():
        # Non-blocking call to reconnect if necessary
        if not connected and not connect_task_created:
            asyncio.get_event_loop().create_task(connect_to_url())
            connect_task_created = True

        ret, frame = capture.get_next_frame()

        if not ret:
            logging.warning('capture object frame missed')
            continue

        frame_nr += 1
        print(frame_nr)

        # Create detectionObj
        #detection_obj = DetectionObj(datetime.now(), frame, frame_nr)
        detection_obj = mock_detection_object(frame)
        # Run detection on object

        # Visualise rectangles and show it
        detection_obj.draw_rectangles()
        cv2.imshow('Frame', detection_obj.frame)

        # Tracking phase
        update_feature_maps()

        # Non-blocking call to send bounding boxes
        asyncio.get_event_loop().create_task(write_message(detection_obj.to_json()))

        # Every 10 frames, send updated feature maps
        if frame_nr % feature_map_delay == 0:
            print("Sending feature maps")
            asyncio.get_event_loop().create_task(write_message(json.dumps(mock_feature_map_dict)))

        # Close loop when q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Hand control back to event loop
        await asyncio.sleep(0)

if __name__ == '__main__':
    asyncio.run(main())