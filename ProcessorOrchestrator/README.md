# Processor Orchestrator

This component is responsible for managing communications between camera processor and interfaces using WebSockets.

## Quickstart

### Starting

#### Docker

Run the following command to startup the orchestrator

```bash
docker run -p 80:80 tracktech/orchestrator:latest
```

Port 430 should also be made available if SSL is used. See below for other optional environment variables.

#### Local

Make sure python is installed and the repository is cloned. Install the dependencies using.

```bash
pip install -r requirements.txt
pip install Auth-1.0.tar.gz
```

Set the current folder as the python root path.

Optionally set other environment variables.

Run the program

```bash
python src/main.py
```

### Environment variables

The following environment variables can be used:

| Variable         | Description                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------ |
| SSL_CERT         | A SSL certificate that should be used to create secure WebSockets.                         |
| SSL_KEY:         | The private key for the given SSL certificate.                                             |
| PUBLIC_KEY       | The public key used for authentication.                                                    |
| AUDIENCE         | The token audience.                                                                        |
| CLIENT_ROLE      | The role that should be present in tokens for access to the client socket.                 |
| PROCESSOR_ROLE   | The role that should be present in tokens for access to the processor socket.              |
| TRACKING_TIMEOUT | The optional time in seconds after which an object should automatically stop being tracked |

## Communications

Communication with the orchestrator can be done over two WebSocket handlers channels:

- ws(s)://HOST/client
- ws(s)://HOST/processor

Both sockets expect messages in JSON format. A message should contain at least a
"type" property, which specifies the message type. The server does not respond if the type is unknown.

### Client

The client WebSocket knows the following types of messages:

- "start": This command is used to start the tracking of an object in the specified frame,
  needs the following additional properties:

  - "cameraId": The identifier of the processor on which the bounding box of the object to be tracked was computed.
  - "frameId": The identifier of the frame on which the bounding box of the object to be tracked was computed.
  - "boxId": The identifier of the bounding box computed for the object to be tracked.
  - "image": A serialised image that the processor can use for re-identification.

  Of these properties, at least either "image" parameter or "frameId" and "boxId" parameters are required to be sent.

- "stop" | This command is used to stop the tracking of an object; it needs the following additional property:
  - "objectId" | The identifier of the object which should no longer be tracked.
- "setUsesImages" | This command is used to specify whether or not this client uses images and should therefore
  receive cutouts when they are sent alongside a "start" command. It needs the following property:
  - "usesImages" | A bool indicating whether images are used. If it set to true, then the orchestrator will immediately send all the currently stored images to this client.

### Processor

The processor WebSocket knows the following types of messages:

- "identifier": This signifies a message containing the identifier by which this processor
  should be identified, needs the following additional properties:
  - "id" | The identifier of the processor under which this socket should be registered.
- "boundingBoxes": This signifies a message that contains bounding boxes,
  needs the following additional properties:
  - "frameId" | The identifier of the frame for which these bounding boxes were computed.
  - "boxes" | An object containing the bounding boxes that were computed for this frame.
- "featureMap": This signifies a message that contains a feature map of an object,
  needs the following additional properties:
  - "objectId" | The identifier of the object for which this feature map was computed.
  - "featureMap" | An object containing the new feature map that was computed.

### Tracking Timelines

Finally, there is also an HTTP handler that serves to log the data of a given object.
This data is located at

- http(s)://HOST/timelines?object_id=ID

Where ID is the id of the object of which the timeline is required.  
Timeline tracking data is returned as a JSON with one property, "data" that contains an array of objects with a "timeStamp" property and a "processorId" property containing the id of the processor on which the object was detected.

## Architecture

The architecture of the application is made up of the following main components:

- main.py: starts the server and handles routing to handlers.
- client_socket.py: contains the WebSocket handler for clients.
- processor_socket.py: contains the WebSocket handler for processors.
- object_manager.py: contains a class for tracking objects that contains the identifier, feature map, and functionality for automatic stopping of tracking.
- connections.py: contains dictionaries for the currently connected sockets.
- logger.py: contains methods for standardised logging.
- timeline_handler.py: contains HTTP Handler that serves timeline tracking info of a specified object.

## Dependencies

Dependencies for running the main application are listed in requirements.txt;
dependencies for running the tests are listed in requirements-test.txt. All dependencies
should be installed with pip.

## Running tests

The project contains two testing stages, unit testing and integration testing.
Tests should be run through docker compose, as they may rely on other services handled in the compose file.
The stages can be run as follows:

- Unit testing: run "docker-compose -f compose/docker-compose_test_unit.yml"
- Integration testing: run "docker-compose -f compose/docker-compose_test_integration.yml"
