# Interface

This component contains the web interface for the project. The interface is created with Typescript React and uses the Ant Design UI package for most of its UI components.

## Quickstart

### Starting

There are two ways to run the interface:

#### Docker

run

```bash
docker create -p 5000:5000 --name interface tracktech/interface:latest
```

to create the container

and copy in a config using

```bash
docker cp {config file} interface:build/settings.json
```

and finally, start the container with:

```bash
docker start interface
```

#### Local

Make sure you have npm installed and run

```bash
npm start
```

to start the interface. Make sure the settings file in the public folder is configured.

### Settings

React uses the local environment during building and should be configured using a settings file instead of environment variables.
The settings (places in public in react) should look like this.

```json
{
  "cameras": [
    {
      "Name": "The name of a camera",
      "Id": "The id of the camera (corresponding to the one set in the processor)",
      "Forwarder": "The url of the actual video stream"
    }
  ],
  "objectTypes": ["object types, like person or bicycle"],
  "orchestratorWebsocketUrl": "The Url to the client websocket endpoint on the orchestrator",
  "orchestratorObjectIdsUrl": "The Url to the orchestrator objectids HTTP endpoint",
  "orchestratorTimelinesUrl": "The Url to the orchestrator timelines HTTP endpoint",
  "bufferTime": "number setting the buffer length",
  "segmentLength": "number corresponding to hls segment size of video forwarder",
  "clientId": "ClientId used when getting a token",
  "accessTokenUri": "URI token endpoint of identity providing service",
  "authorizationUri": "URI authorization endpoint of identity providy service",
  "redirectUri": "URI to redirect after token gathering"
}
```

The final four settings can be left empty to start the app without the need to authenticate to use the interface.

## Architecture

The architecture of the application consists of the following main components:

- /react: This folder contains many config files and folders containing the actual source code.
- /react/public: Includes an index.html and static files that are publicly visible.
- /react/src: The source code for the interface, which consists of:
  - /react/src/pages: The main pages of the application.
  - /react/src/components: The custom React components used throughout the application.
  - /react/src/classes: pure typescript classes.
- /react/testing: Folder containing testing files, divided into:
  - /react/testing/unit testing: Jest unit tests that tests individual components.
  - /react/testing/integration testing: Jest tests that test the integration of the interface with the orchestrator.

## Dependencies

### Packages

All dependencies are included in the (react/package.json) and (react/package-lock.json) files and installed with `npm install`.

## Running tests

The project contains two testing stages, unit testing and integration testing.
Tests should be run through docker compose, as they may rely on other services which are handled in the compose file.
The stages can be run as follows:

- Unit testing: run `docker-compose -f compose/docker-compose_test_unit.yml`
- Integration testing: run `docker-compose -f compose/docker-compose_test_integration.yml`

## Linting

The project is linted using ESLint in combination with Prettier. The config files `react/.eslintrc.json` and `react/prettierrc.json` contain the set preferences.
