"""Websocket client class that can connect to a websocket client url and write/read messages asynchronously.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import asyncio
import json
import logging
from collections import deque
from tornado import websocket

from processor.websocket.start_command import StartCommand
from processor.websocket.identify_command import IdentifyCommand
from processor.websocket.stop_command import StopCommand
from processor.websocket.update_command import UpdateCommand


class WebsocketClient:
    """Async websocket client that connects to a specified url and read/write messages.

    Note:
        Should not be instantiated directly. Rather, use the create_client function.

    Attributes:
        connection (WebsocketClient.Connection): Connection object of the websocket.
        reconnecting (bool): Whether we have to reconnect.
        websocket_url (str): Url of the websocket.
        write_queue ([str]): Stores messages that could not be sent due to a closed socket.
        message_queue (Queue): Stores commands sent from orchestrator.
        identifier (str): Identifier of the camera processor for the orchestrator.
    """

    def __init__(self, websocket_url, identifier=None):
        """Initialize the websocket client class with relevant parameters.

        Args:
            websocket_url (str): url of the websocket.
            identifier (str): Identifier of the camera-processor.
        """
        self.connection = None
        self.reconnecting = False
        self.websocket_url = websocket_url
        # List of messages that could not get sent.
        self.write_queue = []
        self.message_queue = deque()
        self.identifier = identifier

    async def connect(self):
        """Connect to the websocket url asynchronously."""
        timeout_left = 60
        sleep = 1
        connected = False

        # Whilst there is no connection.
        while not connected and timeout_left > 0:
            # Reconnect.
            try:
                self.connection =\
                    await websocket.websocket_connect(self.websocket_url,
                                                      on_message_callback=self.__on_message)
                logging.info(f'Connected to {self.websocket_url} successfully')

                # Send an identification message to the orchestrator on connect.
                # Only do this when the websocket is a processor socket.
                if self.identifier is not None:
                    self.send_command(IdentifyCommand(self.identifier))

                connected = True
            # Reconnect failed.
            except ConnectionRefusedError:
                logging.warning(f"Could not connect to {self.websocket_url}, trying again in 1 second...")
                await asyncio.sleep(sleep)
                timeout_left -= sleep

        # If timeout was reached without connection.
        if not connected:
            logging.error("Could never connect with orchestrator")
            raise TimeoutError("Never connected with orchestrator")

    async def disconnect(self):
        """Disconnects the websocket."""
        loop = asyncio.get_event_loop()

        # If event loop was already not closed.
        if not loop.is_closed():
            # Wait until all tasks are complete.
            for task in asyncio.all_tasks():
                if not task.done():
                    await asyncio.sleep(0)

            # Cancels any new tasks in the asyncio loop.
            loop.stop()

        # Close connection.
        self.connection.close()

    async def __write_message(self, message):
        """Internal write message that also writes all messages on the write queue if possible.

        Args:
            message: the message to write.
        """
        try:
            if self.connection is None:
                raise websocket.WebSocketClosedError

            # Write all not yet sent messages.
            for old_msg in self.write_queue:
                self.connection.write_message(old_msg)
                logging.info(f'Writing old message: {message}')

            # Clear the write queue.
            self.write_queue = []

            # Write the new message.
            await self.connection.write_message(message)
            logging.info(f'Writing message: {message}')

        except websocket.WebSocketClosedError:
            # Non-blocking call to reconnect if necessary.
            if not self.reconnecting:
                self.reconnecting = True
                await self.connect()
                self.reconnecting = False

            logging.info(f'Appending to message queue: {message}')
            self.write_queue.append(message)

    def __on_message(self, message):
        """On message callback function.

        Args:
            message (Union[str, bytes]): the raw message posted on the websocket.
        """
        # Websocket closed, reconnect is handled by write_message.
        if not message:
            logging.error("The websocket connection was closed")
            return

        try:
            message_object = json.loads(message)

            class_dict = {
                "start": StartCommand,
                "stop": StopCommand,
                "featureMap": UpdateCommand
            }

            if "type" not in message_object.keys():
                raise KeyError("type missing")

            msg_type = message_object["type"]

            if msg_type not in class_dict.keys():
                raise ValueError("Invalid message type")

            command = class_dict[msg_type].from_message(message_object)

            self.message_queue.append(command)
            logging.info(f"Received command: {str(command)}")

        except ValueError as value_error:
            logging.warning(f'Someone wrote bad json: {message}.\nWith error: {value_error}.')
        except KeyError as key_error:
            logging.warning(f'Someone missed a property in their json: {message}.\nWith error: {key_error}.')
        except TypeError as type_error:
            logging.warning(f'One or more keys is of the wrong type: {message}.\nWith error: {type_error}.')

    def send_command(self, command):
        try:
            asyncio.get_running_loop().create_task(self.__write_message(command.to_json()))
        except RuntimeError:
            return

