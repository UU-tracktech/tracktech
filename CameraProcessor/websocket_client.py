import asyncio
import json
import sys
import logging
from tornado import websocket

# Setup (basic) logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='file.log',
                    level=logging.INFO,
                    filemode='w')

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

state = 0

# url = 'ws://tracktech.ml:50010/processor'
# Url of websocket server
url = 'ws://localhost:80/processor'

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


async def main():
    global connection, connected, connect_task_created

    # Try to get an initial connection
    await connect_to_url()

    # Video processing loop
    while True:
        global state

        # Non-blocking call to reconnect if necessary
        if not connected and not connect_task_created:
            asyncio.get_event_loop().create_task(connect_to_url())
            connect_task_created = True

        state = state + 1
        print(f"STATE: {state}")

        # Simulate delay of video processing, video processing below
        await asyncio.sleep(5)

        # Non-blocking call to write message in parallel, normally happens after frame processing
        asyncio.get_event_loop().create_task(write_message('{"type":"test", "frameId": 12, "boxId": 18}'))

if __name__ == '__main__':
    asyncio.run(main())
