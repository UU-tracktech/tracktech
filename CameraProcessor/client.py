import asyncio
import json
import time
import sys
import logging
from tornado import websocket

# Setup logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='file.log',
                    level=logging.INFO,
                    filemode='w')

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

state = 0

# url = 'ws://tracktech.ml:50010/processor'
url = 'ws://localhost:8000/processor'


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


def read_msg(message):
    if not message:
        logging.error("The websocket connection was closed")
        return
        #asyncio.get_event_loop().stop()

        # Exit from the program if the websocket is closed
        # sys.exit(1)
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
    #except TypeError:
     #   logging.warning(f"Message could not be recognized as json: {message}")


# Write messages to the connection
async def write_message(msg):
    global connection
    try:
        await connection.write_message(msg)
    except websocket.WebSocketClosedError:
        print("TEST ETST TEST")
        await connect_to_url(url)


# Connect to the specified websocket url
async def connect_to_url(url):
    global connection
    connected = False
    while not connected:
        try:
            connection = await websocket.websocket_connect(url, on_message_callback=read_msg)
            logging.info(f"Connected to {url} successfully")
            connected = True
        except ConnectionRefusedError:
            logging.warning(f"Could not connect to {url}, trying again in 1 second...")
            time.sleep(1)


async def main():
    global connection

    await connect_to_url(url)
    # connected = False
    # while not connected:
    #     try:
    #         connection = await websocket.websocket_connect(url, on_message_callback=read_msg)
    #         logging.info(f"Connected to {url} successfully")
    #         connected = True
    #     except ConnectionRefusedError:
    #         logging.warning(f"Could not connect to {url}, trying again in 1 second...")
    #         time.sleep(1)


     # Video processing loop
    while True:
        global state
        # Non-blocking call to write message in parallel
        asyncio.get_event_loop().create_task(write_message('{"type":"test", "frameId": 12, "boxId": 18}'))
        state = state + 1
        print(f"STATE: {state}")
        # Simulate delay
        await asyncio.sleep(5)


if __name__ == '__main__':
    while True:
        asyncio.get_event_loop().run_until_complete(main())
        print("Stopped loop")


connection = None
