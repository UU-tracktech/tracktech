# Webhosting

The content of this folder uses the [Tornado](https://www.tornadoweb.org/en/stable/) library for the communication with the outside world.
There are two ways we use Tornado.

One creates a websocket connection with the Processor Orchestrator component.
This is used during deployment of the Camera Processor.

The other method is for docker debugging and remote verification purposes.
This creates a http server which can be connected to see the output of a single Camera Processor online without having to boot up the entire system.

### Websockets
The [WebsocketClient](websocket_client.py) creates a websocket connection with the Processor Orchestrator component.
Given a websocket url the [WebsocketClient](websocket_client.py) will try to connect for a minute.
It contains its own logic in case the connection gets lost where it keeps track of the messages that were not sent over.

When messages are received from Processor Orchestrator component the desired handler is being called. This still has to get implemented.

#### Websocket url
The websocket url is constructed the following way

`(ws|wss):(<docker-service-name>|<device IP>|localhost):(<port-number>)/(<url-extension>)`

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
