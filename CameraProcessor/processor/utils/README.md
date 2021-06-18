# Utils

This folder is for all kinds of additional functionalities that are supporting the main application.

### authentication.py
Connects with an authentication server specified in the environment. Uses the credentials to get a token via the client_credentials flow for OAuth.

### config_parser.py
Parses configurations from configs.ini in the root of camera processor. Reads from environment variables. All of these are specified in the root README.md.

### convert.py
Converts objects that contains functionalities to convert objects to a dictionary the frame buffer expects.

### create_runners.py
Creates runners for each stage separately based on switch statements.

### dataloader.py
Responsible for creating a dataloader object based on what is specified in configurations.

### display.py
Creates a 2 by 2 image from the different stages in the pipeline. Stitches the images together.

### draw.py
Draws bounding boxes on frames and includes a tag. Contains a draw method for each different stage.

### features.py
Utilities for feature maps, creates cutouts and resizes it to create a correct size for the model.

### text.py
Converts data_objects to string/dicts that get converted to text to send through the websocket.