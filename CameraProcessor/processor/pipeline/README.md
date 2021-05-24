# Pipeline

The pipeline couples all stages together and properly propagates the output using the supported methods.
[process_frames.py](process_frames.py) is called from [main.py](../main.py) to start the pipeline and is responsible for calling all stages.
The stages currently supported are detection and tracking. 

A frame buffer storing previous frames is also already included. 
This frame buffer stores a set amount of frames that can be used to perform re-identification. 
This is necessary since the tracked subject isn't always known when the frame was initially processed.

## Supported outputs

- OpenCV: output processed frames to OpenCV. Exit OpenCV window (and stop application) by pressing 'q'.
- Tornado: output processed frames on the Tornado webpage. 
  Only visual output method if the system is run in Docker.
  Inefficient due to necessary encoding.
- Deploy: send bounding boxes and feature maps to the orchestrator.


## Stages

The final pipeline should encompass the tracking of subjects over multiple cameras.
This entails three stages (like discussed in the [architecture](../../README.md)): 
detection, tracking, and re-identification.

### Detection

The [detection stage](detection/README.md) is responsible for performing detections of all supported objects in the current frame.
This stage is necessary to run the tracking algorithm and is thus also required to work quite fast.

### Tracking

The [tracking stage](tracking/README.md) performs a simple tracking algorithm. 
The requirements of this algorithm are that it is very fast, 
and its goal is that it gathers information about potential subjects that can later be utilized in the re-identification.
The tracker is responsible for remembering information about past frames to give all trackers in the present frame.

### Re-identification

To be implemented in a later version.
