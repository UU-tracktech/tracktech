# Websocket

Creates a WebSocket connection with the Processor Orchestrator component.
This is used during the deployment of the Camera Processor.
- [websocket_client.py](../websocket/websocket_client.py): Defines the WebSocket logic
- [start_command.py](start_command.py): Start command object
- [stop_command.py](stop_command.py): Stop command object

### Websockets
The [WebsocketClient](../websocket/websocket_client.py) creates a WebSocket connection with the Processor Orchestrator component.
Given a WebSocket URL, the [WebsocketClient](../websocket/websocket_client.py) will try to connect for a minute.
It contains logic in case the connection gets lost where it keeps track of the messages that were not sent over.

When messages are received from the Processor Orchestrator component the desired handler is being called. This still has to get implemented.

#### Websocket url
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

### Websocket commands

Because the WebsocketClient does not contain the state of the application the messages received have to get be reminded.
[StartCommand](start_command.py) and [StopCommand](stop_command.py) are written to a list and saved for when the main loop can process them.

The API commands the WebSocket uses are listed extensively in the Processor Orchestrator [README.md](../../../ProcessorOrchestrator/README.md)