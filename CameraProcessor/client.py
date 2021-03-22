import asyncio
import json
from tornado import websocket


def update_feature_map(message):
    object_id = message["objectId"]
    feature_map = message["featureMap"]
    print(f"Updating object {object_id} with feature map {feature_map}")


def start_tracking(message):
    object_id = message["objectId"]
    frame_id = message["frameId"]
    box_id = message["boxId"]
    print(f"Start tracking box {box_id} in frame_id {frame_id} with new object id {object_id}")


def stop_tracking(message):
    object_id = message["objectId"]
    print(f"Stop tracking object {object_id}")


def read_msg(message):
    print("Server sent: " + message)
    try:
        message_object = json.loads(message)

        # switch on message type
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
            print("Someone gave an unknown command")
        else:
            function()

    except ValueError:
        print("Someone wrote bad json")
    except KeyError:
        print("Someone missed a property in their json")


# Write messages to the connection
async def write_message(msg):
    await connection.write_message(msg)


async def main():
    global connection
    connection = await websocket.websocket_connect('ws://localhost:8000/processor', on_message_callback=read_msg)

    # Video processing loop - should we send bounding boxes here?
    while True:
        # non blocking call to write message in parallel
        asyncio.get_event_loop().create_task(write_message('{"type":"test", "frameId": 12, "boxId": 18}'))

        # Simulate delay
        await asyncio.sleep(100)

if __name__ == '__main__':
    asyncio.run(main())

connection = None
