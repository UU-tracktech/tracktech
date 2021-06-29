# WebSocket

Creates a WebSocket connection with the Processor Orchestrator component.
This WebSocket connection is used during the deployment of the Camera Processor.
- [websocket_client.py](../websocket/websocket_client.py): Defines the WebSocket logic
- [start_command.py](start_command.py): Start command object
- [stop_command.py](stop_command.py): Stop command object

### WebSockets
The [WebsocketClient](../websocket/websocket_client.py) creates a WebSocket connection with the Processor Orchestrator component.
Given a WebSocket URL, the [WebsocketClient](../websocket/websocket_client.py) will try to connect for a minute.
It contains logic if the connection gets lost where it keeps track of the unsent messages.

When messages are received from the Processor Orchestrator component, the desired handler is called. However, this functionality still has to get implemented.

#### WebSocket URL
The WebSocket URL is constructed the following way:

`(ws|wss)://(<docker-service-name>|<device IP>|localhost):(<port-number>)/(<url-extension>)`

- ws|wss
  * ws: Http without SSL
  * wss: Http with SSL enabled
- \<docker-service-name\>|\<device IP\>|localhost
  * <docker-service-name>: Name of the docker service when running inside docker swarm
  * <device IP>: Device IP where the Processor Orchestrator is ran
  * localhost: Ip of local device on Windows
- \<port-number\>
  * port-number: Port on which to connect
- \<url-extension\>
  * url-extension: The extension of the websocket URL to connect to. In the case of the Processor Orchestrator: '/processor'

### WebSocket messages

Because the WebsocketClient does not contain the application's state, the messages received have to be remembered and processed later.
[StartMessage](start_message.py), [StopMessage](stop_message.py) and [UpdateMessage](update_message.py) are written to a list and saved for when the main loop can process them.

The WebSockets' API commands are listed extensively in the Processor Orchestrator [README.md](../../../ProcessorOrchestrator/README.md)

#### IMessage

The interface class defining behavior of a message to get implemented in order to work with the message queue.
It converts the message to a json string and can convert it back.

#### Boxes message

The processor sends boxes to the orchestrator indicating where on the frame objects are found.
It sends the box information like classificaiton, certainty, and position combined with the frame id.
When a box is a tracked box, an additional identifier is sent so the interface can display this to the user.

#### Start message

The interface sends start commands to the processor through the ProcessorOrchestrator.
Whenever this message is recieved the processor tries to extract the featuremap of the object and sends an update message to the orchestrator.

#### Stop message

The interface sends stop commands whenever an object does not have to get tracked anymore.
In this case the processor removes the information and does not try to re-identify the object anymore.

#### Update message

This message is sent by the cameraprocessor to the processororchestrator whenever it extracts the featuremap of a object that needs to get tracked.
Because of the behavior of the orchestrator. A sent update message gets shared with all other processors.
These processors will then add this featuremap and try to re-identify the object on the stream.