# Interface

This component contains the web interface for the project. The interface is created with Typescript React and uses the Ant Design UI package for most of its UI components.

## How to use

There are two ways to run the interface:

- (using docker) run `docker-compose up` in the current folder

## Architecture

The architecture of the application is made up of the following main components:

- /react: This folder contains many config files as well as folders containing the actual source code.
- /react/public: Includes an index.html, as well as static files that are publicically visible.
- /react/src: The source code for the interface, which consists of:
  - /react/src/pages: The main pages of the application.
  - /react/src/components: The custom react components used throughout the application.
  - /react/src/classes: pure typescript classes.
- /react/testing: Folder containing testing files, divided into:
  - /react/testing/unit testing: Jest unit tests that test individual components.
  - /react/testing/integration testing: Jest tests that test integration of the interface with the orchestrator.

## Dependencies

### Packages

All dependencies are included in the (react/package.json) and (react/package-lock.json) files and can be installed with `npm install`

## Running tests

The project contains two testing stages, unit testing and integration testing.
Tests should be run through docker compose, as they may rely on other services which are handled in the compose file.
The stages can be run as follows:

- Unit testing: run `docker-compose -f compose/docker-compose_test_unit.yml`
- Integration testing: run `docker-compose -f compose/docker-compose_test_integration.yml`

## Linting

The project is linted using ESLint in combination with Prettier. The config files `react/.eslintrc.json` and `react/prettierrc.json` contain the set preferences.
