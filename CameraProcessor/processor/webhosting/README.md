# Webhosting

The content of this folder uses the [Tornado](https://www.tornadoweb.org/en/stable/) library for the communication with the outside world.
There are two ways we use Tornado.

One creates a websocket connection with the Processor Orchestrator component.
This is used during deployment of the Camera Processor.
- [websocket_client.py](websocket_client.py): Defines the websocket logic
- [start_command.py](start_command.py): Start command object
- [stop_command.py](stop_command.py): Stop command object

The other method is for docker debugging and remote verification purposes.
This creates a http server which can be connected to see the output of a single Camera Processor online without having to boot up the entire system.
- [html_page_handler.py](html_page_handler.py): Serves the webpage in which the stream is visible
- [stream_handler.py](stream_handler.py): Serves the individual frames to the webclient

### Websockets
The [WebsocketClient](websocket_client.py) creates a websocket connection with the Processor Orchestrator component.
Given a websocket url the [WebsocketClient](websocket_client.py) will try to connect for a minute.
It contains its own logic in case the connection gets lost where it keeps track of the messages that were not sent over.

When messages are received from Processor Orchestrator component the desired handler is being called. This still has to get implemented.

#### Websocket url
The websocket url is constructed the following way:

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
  * url-extension: The extension of the websocket-url to connect to. In the case of the Processor Orchestrator: '/processor'

#### Websocket commands
Because the WebsocketClient does not contain the state of the application the messages received have to get be reminded.
[StartCommand](start_command.py) and [StopCommand](stop_command.py) are written to a list and saved for when the main loop can process them.

The API commands the websocket uses are listed extensively in the Processor Orchestrator [README.md](../../../ProcessorOrchestrator/README.md)

### Hosting website

Tornado is also used for remote verification and to visually verify results in Docker. When the detection and tracking is done
the output image can be served to a webclient. The html page of the website is stored inside the [webpage](../../webpage) folder
and given by the [html_page_handler.py](html_page_handler.py).

After the html page is loaded stream gets created and the process_stream loop starts inside the [stream_handler.py](stream_handler.py).
This class contains the serving logic for when the frame is processed. Every 0.1 seconds the processed frames get flushed so the client can retrieve the images. 

The [stream_handler.py](stream_handler.py) implements a RequestHandler which starts a coroutine that contains the main loop of the application.
Because of the coroutine the get does not consist out of a single GET command but instead it repeatedly requests the images from the stream.
