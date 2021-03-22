
# from tornado import escape
# from tornado import gen
# from tornado import ioloop
# from tornado import websocket
# import json
# import time
#
#
#
#
# class WebSocketClient():
#     """Class that can communicate with websockets
#     """
#
#     def __init__(self, url):
#         """:param str url: URL of websocket to connect to"""
#         self._url = url
#
#     def connect(self):
#         """Connect to the websocket"""
#         ws_connect = websocket.websocket_connect(self._url)
#         ws_connect.add_done_callback(self._connect_callback)
#
#     def send(self, data):
#         """Send message to the server
#         :param str data: message.
#         """
#         if not self._ws_connection:
#             raise RuntimeError('No available websocket connection')
#
#         #self._ws_connection.write_message(escape.utf8(json.dumps(data)))
#         self._ws_connection.write_message(f"Hello world, {data}")
#
#     def close(self):
#         """Close connection."""
#
#         if not self._ws_connection:
#             raise RuntimeError('Web socket connection is already closed.')
#
#         self._ws_connection.close()
#
#     def _connect_callback(self, future):
#         """This is called after the connection future is resolved (whether succcesful or not)"""
#         if future.exception() is None:
#             self._ws_connection = future.result()
#             self._on_connection_success()
#             self._read_messages()
#         else:
#             self._on_connection_error(future.exception())
#
#     @gen.coroutine
#     def _read_messages(self):
#         """This method keeps checking for messages on the websocket"""
#         while True:
#             msg = yield self._ws_connection.read_message()
#             if msg is None:
#                 self._on_connection_close()
#                 break
#
#             self._on_message(msg)
#
#     def _on_message(self, msg):
#         """This is called when new message is available from the server.
#         :param str msg: server message.
#         """
#         print(f"Received new message from the server: {msg}")
#         try:
#             message_object = json.loads(msg)
#             if message_object["type"] == "featureMap":
#                 self.update_feature_map(message_object)
#             elif message_object["type"] == "start":
#                 self.start_tracking(message_object)
#             elif message_object["ty[e"] == "stop":
#                 self.stop_tracking(message_object)
#             else:
#                 self.send("Unknown command")
#         except ValueError:
#             self.send("Bad json")
#         except KeyError:
#             self.send("Missed property in json")
#
#
#     def _on_connection_success(self):
#         """This is called on successful connection ot the server.
#         """
#         print(f"Connected to {self._url}")
#
#         self.send("Test")
#
#     def _on_connection_close(self):
#         """This is called when server closed the connection.
#         """
#         print(f"Connection closed")
#
#     def _on_connection_error(self, exception):
#         """This is called in case if connection to the server could
#         not established.
#         """
#         raise Exception(f"Could not connect to {self._url}")
#
#     def update_feature_map(self, message):
#         object_id = message["objectId"]
#         feature_map = message["featureMap"]
#         print(f"Someone send a feature map of an object with Id {object_id}")
#
#     def start_tracking(self, message):
#         object_id = message["objectId"]
#         frame_id = message["frameId"]
#         box_id = message["boxId"]
#         print(f'Someone wants to start tracking the object of bounding box {box_id} in frame {frame_id} with the new object id {object_id}')
#
#     def stop_tracking(self, message):
#         object_id = message["objectId"]
#         print(f'Someone wants to stop tracking the object {object_id}')
#
#
#
#

# class TestWebSocketClient(WebSocketClient):
#
#     def _on_message(self, msg):
#         print(msg)
#         deadline = time.time() + 1
#         ioloop.IOLoop().instance().add_timeout(
#             deadline, functools.partial(self.send, str(int(time.time()))))
#
#     def _on_connection_success(self):
#         print('Connected!')
#         #self.send(str(int(time.time())))
#
#     def _on_connection_close(self):
#         print('Connection closed!')
#
#     def _on_connection_error(self, exception):
#         print('Connection error: %s', exception)


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


def handle_msg(message):
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



async def main():
    connection = await websocket.websocket_connect('ws://localhost:8000/processor', on_message_callback=handle_msg)

    # Video processing loop - should we send bounding boxes here?
    while True:
        await connection.write_message('{"type":"test", "frameId": 12, "boxId": 18}') # Don't await? don't want to block on this
        await asyncio.sleep(100)  # Simulate delay

if __name__ == '__main__':
    asyncio.run(main())
