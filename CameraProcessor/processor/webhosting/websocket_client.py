"""Websocket client class that can connect to a websocket client url and write/read messages asynchronously.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import asyncio
import json
import logging
from collections import deque
from tornado import websocket

from processor.webhosting.start_command_simple import StartCommandSimple
from processor.webhosting.start_command_extended import StartCommandExtended
from processor.webhosting.start_command_search import StartCommandSearch
from processor.webhosting.stop_command import StopCommand
from processor.webhosting.update_command import UpdateCommand
from processor.utils.authentication import get_token


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
        configs (ConfigParser): Configurations of the application, contains the authorization url.
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
        """Connect to the websocket url asynchronously.

        Raises:
            AttributeError: When the authentication has not been successful due to incorrect credentials.
            EnvironmentError: Whenever the environment variables were not found in the environment.
            ConnectionError: No response from the authentication server.
            TimeoutError: After several retries the connection could still not be established.
        """
        # If we want to do authentication, try to get an access token
        auth_server_url = os.environ.get("AUTH_SERVER_URL")
        auth_token = None
        if auth_server_url:
            auth_token = await self.get_access_token(auth_server_url)
        else:
            logging.info("Authentication is disabled since AUTH_SERVER_URL is not specified in environment.")

        timeout_left = 60
        sleep = 1
        connected = False

        # Try to authenticate to the processor orchestrator
        # Whilst there is no connection.
        while not connected and timeout_left > 0:
            # Reconnect.
            try:
                self.connection =\
                    await websocket.websocket_connect(self.websocket_url,
                                                      on_message_callback=self._on_message)
                logging.info(f'Connected to {self.websocket_url} successfully')

                # Send authentication token to the orchestrator on connect (if it exists)
                if auth_token:
                    auth_message = json.dumps({
                        "type": "authenticate",
                        "jwt": auth_token
                    })
                    logging.info('Authentication message sent to orchestrator.')
                    await self.connection.write_message(auth_message)

                # Send an identification message to the orchestrator on connect.
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

    @staticmethod
    async def get_access_token(auth_server_url):
        """Retrieves the access token from the authentication server

        Args:
            auth_server_url (str): Url of the authentication server to request the token from.

        Returns:
            str: Access token to the authentication server.

        Raises:
            AttributeError:
            EnvironmentError: Whenever the environment variables were not found in the environment.
            ConnectionError: No response from the authentication server.
        """
        retries_left = 5

        # While there are more.
        while retries_left > 0:
            try:
                token = get_token(auth_server_url)
                return token
            except ConnectionError:
                retries_left -= 1
                logging.warning('Retrieval of token failed, trying again')
                await asyncio.sleep(2)
            except AttributeError as err:
                logging.error('Authentication credentials CLIENT_ID and CLIENT_SECRET are invalid')
                raise err
            except EnvironmentError as err:
                logging.error('Authentication url is set but the credentials are missing from the environment')
                raise err

        # After several retries the connection could not be established.
        raise ConnectionError("Could not connect to the authentication server successfully.")

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
            message (Union[str, bytes]): JSON parse of sent message.
        """
        object_id = message["objectId"]
        feature_map = message["featureMap"]

        self.message_queue.append(UpdateCommand(feature_map, object_id))

    def generate_tracking_message(self, message):
        """Factory function that returns the correct StartCommand type.

        Args:
            message (Union[str, bytes]): JSON parse of the sent message.

        Returns:
            StartCommand: A subclass of the StartCommand superclass.
        """
        del message["type"]
        if all(k in message.keys() for k in {"frameId", "boxId"}):
            if "image" in message.keys():
                return StartCommandExtended(**message)
            return StartCommandSearch(**message)
        if "image" in message.keys():
            return StartCommandSimple(**message)
        raise ValueError("Start Tracking message does not contain necessary information.")

    def start_tracking(self, message):
        """Handler for the "start tracking" command.

        Args:
            message (Union[str, bytes]): JSON parse of sent message.
        """
        # Remove the "type" item, because we don't need that anymore.
        self.message_queue.append(self.generate_tracking_message(message))

    def stop_tracking(self, message):
        """Handler for the "stop tracking" command.

        Args:
            message (Union[str, bytes]): JSON parse of sent message.
        """
        object_id = message["objectId"]

        self.message_queue.append(StopCommand(object_id))
    # pylint: enable=R0201
