import asyncio
import json
import sys
import logging
from datetime import datetime
import cv2
from tornado import websocket
from processor.pipeline.detection.detection_obj import DetectionObj
from processor.input.hls_capture import HlsCapture


async def create_client(url, id=None):
    """
    Method used to create a websocket client object
    Args:
        url: Websocket url to connect to
        id: Identifier of the websocket. If the websocket is not used as a processor socket,
        set id to None. Otherwise, set to an identifier.

    Returns: Websocket client object
    """
    client = WebsocketClient(url, id)
    await client.connect()
    return client


class WebsocketClient:
    """
    Async websocket client that connects to a specified url and read/write messages
    Should not be instantiated directly. Rather, use the create_client function
    """

    def __init__(self, url, identifier=None):
        self.connection = None  # Holds the connection object
        self.reconnecting = False  # Whether we are currently trying to reconnect
        self.url = url  # The url of the websocket
        self.write_queue = []  # Stores messages that could not be sent due to a closed socket
        self.identifier = identifier  # Identify to identify itself with orchestrator

        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.INFO,
                            handlers=[logging.FileHandler(filename="client.log", encoding='utf-8', mode='w')])


        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    async def connect(self):
        """
        Connect to the websocket url asynchronously
        """
        timeout_left = 60
        sleep = 1
        connected = False
        while not connected and timeout_left > 0:
            try:
                self.connection =\
                    await websocket.websocket_connect(self.url,
                                                      on_message_callback=self._on_message)
                logging.info(f'Connected to {self.url} successfully')

                # Send an identification message to the orchestrator on connect
                # Only do this when the websocket is a processor socket
                if self.identifier is not None:
                    id_message = json.dumps({
                        "type": "identifier",
                        "id": self.identifier
                    })
                    logging.info(f'Identified with: {id_message}')
                    await self.connection.write_message(id_message)

                connected = True

            except ConnectionRefusedError:
                logging.warning(f"Could not connect to {self.url}, trying again in 1 second...")
                await asyncio.sleep(sleep)
                timeout_left -= sleep

        # If timeout was reached without connection
        if not connected:
            logging.error("Could never connect with orchestrator")
            raise TimeoutError("Never connected with orchestrator")

    def write_message(self, message):
        """
        Write a message on the websocket asynchronously

        Args:
            message: the message to write
        """
        try:
            asyncio.get_running_loop().create_task(self._write_message(message))
        except RuntimeError:
            return

    async def _write_message(self, message):
        """
        Internal write message that also writes all messages on the write queue if possible

        Args:
            message: the message to write
        """
        try:
            if self.connection is None:
                raise websocket.WebSocketClosedError

            # Write all not yet sent messages
            for old_msg in self.write_queue:
                self.connection.write_message(old_msg)
                logging.info(f'Writing old message: {message}')

            # Clear the write queue
            self.write_queue = []

            # Write the new message
            await self.connection.write_message(message)
            logging.info(f'Writing message: {message}')

        except websocket.WebSocketClosedError:
            # Non-blocking call to reconnect if necessary
            if not self.reconnecting:
                self.reconnecting = True
                await self.connect()
                self.reconnecting = False

            logging.info(f'Appending to message queue: {message}')
            self.write_queue.append(message)

    def _on_message(self, message):
        """
        On message callback function

        Args:
            message: the raw message posted on the websocket
        """
        # Websocket closed, reconnect is handled by write_message
        if not message:
            logging.error("The websocket connection was closed")
            return

        try:
            message_object = json.loads(message)

            # Switch on message type
            actions = {
                "featureMap":
                    lambda: self.update_feature_map(message_object),
                "start":
                    lambda: self.start_tracking(message_object),
                "stop":
                    lambda: self.stop_tracking(message_object)
            }

            # Execute correct function
            function = actions.get(message_object["type"])
            if function is None:
                logging.warning(f'Someone gave an unknown command: {message}')
            else:
                function()

        except ValueError:
            logging.warning(f'Someone wrote bad json: {message}')
        except KeyError:
            logging.warning(f'Someone missed a property in their json: {message}')

    # Mock methods on received commands
    # pylint: disable=R0201
    def update_feature_map(self, message):
        """
        Handler for received feature maps

        Args:
            message: JSON parse of the sent message
        """
        object_id = message["objectId"]
        feature_map = message["featureMap"]
        logging.info(f'Updating object {object_id} with feature map {feature_map}')

    def start_tracking(self, message):
        """
        Handler for the "start tracking" command

        Args:
            message: JSON parse of the sent message
        """
        object_id = message["objectId"]
        frame_id = message["frameId"]
        box_id = message["boxId"]
        logging.info(f'Start tracking box {box_id} in frame_id {frame_id} with new object id {object_id}')

    def stop_tracking(self, message):
        """
        Handler for the "stop tracking" command

        Args:
            message: JSON parse of the sent message
        """
        object_id = message["objectId"]
        logging.info(f'Stop tracking object {object_id}')
    # pylint: enable=R0201

def dead_code(a, b):
    c = a * b - b
    d = c * a
    if c == d:
        return a - b
    else:
        return d - c
    return a-b

async def main():
    """
    Main function that runs the video processing loop and listens on the websocket in parallel
    """
    dead_code(1,1)
    dead_code(1, 1)
    dead_code(1, 1)
    dead_code(1, 1)
    dead_code(1, 1)
    dead_code(1, 1)
    dead_code(1, 1)
    dead_code(1, 1)
    dead_code(1, 1)
    dead_code(1, 1)
    dead_code(1,1)


    capture = HlsCapture()
    # ws_client = await create_client("wss://echo.websocket.org")
    ws_client = await create_client('ws://localhost:80/processor')
    frame_nr = 0
    feature_map_delay = 10

    # Video processing loop
    while capture.opened():

        ret, frame, _ = capture.get_next_frame()

        if not ret:
            logging.warning('capture object frame missed')
            continue

        frame_nr += 1
        print(frame_nr)

        # Create detectionObj
        detection_obj = DetectionObj(datetime.now(), frame, frame_nr)
        # detection_obj = mock_detection_object(frame)
        # Run detection on object

        # Visualise rectangles and show it
        detection_obj.draw_rectangles()
        cv2.imshow('Frame', detection_obj.frame)

        # Tracking phase

        # Non-blocking call to send bounding boxes
        # asyncio.get_event_loop().create_task(write_message(detection_obj.to_json()))

        # test with echo web server
        ws_client.write_message('{"type":"test", "frameId":2, "boxId":3}')

        # Every 10 frames, send updated feature maps
        if frame_nr % feature_map_delay == 0:
            pass
            # print("Sending feature maps")
            # asyncio.get_event_loop().create_task(write_message(json.dumps(mock_feature_map_dict)))

        # Close loop when q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Hand control back to event loop
        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
