# Utils

This folder is for all kinds of additional functionalities that are supporting the main application.

### authentication.py
This file connects with an authentication server specified in the environment. Uses the credentials to get a token via the client_credentials flow for OAuth.

### config_parser.py
This file parses configurations from configs.ini in the root of the camera processor. Reads from environment variables. All of these are specified in the root README.md.

### convert.py
Converts objects that contain functionalities to convert objects to a dictionary the frame buffer expects.

### create_runners.py
This file creates runners for each stage separately based on switch statements.

### dataloader.py
Responsible for creating a dataloader object based on what is specified in configurations.

### display.py
Creates a two-by-two image from the different stages in the pipeline and stitches the images together.

### draw.py
Draws bounding boxes on frames and includes a tag. It contains a draw method for each different stage.

### features.py
Utilities for feature maps. It creates cutouts and resizes them to create the correct size for the model.

### text.py
Converts data_objects to strings/dictionaries that get converted to text to send through the WebSocket.
