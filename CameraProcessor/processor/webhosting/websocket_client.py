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

from processor.utils.authentication import get_token
from processor.webhosting.start_command import StartCommand
from processor.webhosting.stop_command import StopCommand
from processor.webhosting.update_command import UpdateCommand


class WebsocketClient:
    """Async websocket client that connects to a specified url and read/write messages.

    Note:
        Should not be instantiated directly. Rather, use the create_client function.

    Attributes:
        connection (WebsocketClient.Connection): Connection object of the websocket.
        reconnecting (bool): Whether or not we have to reconnect.
        websocket_url (str): Url of the websocket.
        write_queue ([str]): Stores messages that could not be sent due to a closed socket.
        message_queue (Queue): Stores commands sent from orchestrator.
        identifier (str): Identifier of the camera processor for the orchestrator.
        configs (ConfigParser): Configurations of the application, contains the authorization url.
    """

    def __init__(self, websocket_url, configs, identifier=None):
        """Initialize the websocket client class with relevant parameters.

        Args:
            websocket_url (str): url of the websocket.
            configs (ConfigParser): Configurations of the application.
            identifier (str): Identifier of the camera-processor.
        """
        self.connection = None
        self.reconnecting = False
        self.websocket_url = websocket_url
        # List of messages that could not get sent.
        self.write_queue = []
        self.message_queue = deque()
        self.identifier = identifier
        self.configs = configs

    async def connect(self):
        """Connect to the websocket url asynchronously."""
        timeout_left = 60
        sleep = 1
        connected = False

        #try:
        #    auth_token = get_token(self.configs['Authentication']['auth_server_url'])
        #except EnvironmentError:
        auth_token = self.get_access_token()

        # If get_acces_token returns None and does not start with wss, we are good
        # if it starts with wss, then we return an error since we cannot authentica

        # Whilst there is no connection.
        while not connected and timeout_left > 0:
            # Reconnect.
            try:
                self.connection =\
                    await websocket.websocket_connect(self.websocket_url,
                                                      on_message_callback=self._on_message)
                logging.info(f'Connected to {self.websocket_url} successfully')

                if self.websocket_url.startswith('wss'):
                    auth_message = json.dumps({
                        "type": "authenticate",
                        "jwt": auth_token
                    })
                    logging.info('')
                    await self.connection.write_message(auth_message)
                # Send an identification message to the orchestrator on connect.
                # Only do this when the websocket is a processor socket.
                if self.identifier is not None:
                    id_message = json.dumps({
                        "type": "identifier",
                        "id": self.identifier
                    })
                    logging.info(f'Identified with: {id_message}')
                    await self.connection.write_message(id_message)

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

    async def get_access_token(self):
        """

        Returns:
            str: Access token to the authentication server.
        """
        retries_left = 5

        while retries_left > 0:
            try:
                token = get_token(self.configs['Authentication']['auth_server_url'])
                return token
            except ConnectionError:
                retries_left -= 1
                logging.warning('Retrieval of token failed, trying again')
                await asyncio.sleep(2)
            except EnvironmentError:
                logging.warning('No authentication will take place because environment variables are missing')
                return None

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

    def write_message(self, message):
        """Write a message on the websocket asynchronously.

        Args:
            message (str): the message to write.
        """
        try:
            asyncio.get_running_loop().create_task(self._write_message(message))
        except RuntimeError:
            return

    async def _write_message(self, message):
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

    def _on_message(self, message):
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

            # Switch on message type.
            actions = {
                "featureMap":
                    lambda: self.update_feature_map(message_object),
                "start":
                    lambda: self.start_tracking(message_object),
                "stop":
                    lambda: self.stop_tracking(message_object)
            }

            # Execute correct function.
            function = actions.get(message_object["type"])
            if function is None:
                logging.warning(f'Someone gave an unknown command: {message}')
            else:
                function()

        except ValueError:
            logging.warning(f'Someone wrote bad json: {message}')
        except KeyError:
            logging.warning(f'Someone missed a property in their json: {message}')

    # Mock methods on received commands.
    # pylint: disable=R0201
    def update_feature_map(self, message):
        """Handler for received feature maps.

        Args:
            message (Union[str, bytes]): JSON parse of the sent message.
        """
        object_id = message["objectId"]
        feature_map = message["featureMap"]

        self.message_queue.append(UpdateCommand(feature_map, object_id))

    def start_tracking(self, message):
        """Handler for the "start tracking" command.

        Args:
            message (Union[str, bytes]): JSON parse of the sent message.
        """
        frame_id = message["frameId"]
        box_id = message["boxId"]
        object_id = message["objectId"]

        self.message_queue.append(StartCommand(frame_id, box_id, object_id))

    def stop_tracking(self, message):
        """Handler for the "stop tracking" command.

        Args:
            message (Union[str, bytes]): JSON parse of the sent message.
        """
        object_id = message["objectId"]

        self.message_queue.append(StopCommand(object_id))
    # pylint: enable=R0201
