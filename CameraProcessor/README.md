# Camera Processor

The job of the camera processor is to detect all potential subjects
and track the subjects that have been selected by the camera operators using the Interface.
The camera operators only see the detections within a frame, and the subjects they started tracking.
The tracking of subjects is performed over multiple cameras, 
notifying the camera operator when a subject is re-identified.

## Architecture

The inner workings of the camera processor consist of three parts. 
The input processed by the pipeline and sent to either other camera processors or the interface.

### Input

There are two inputs available to the camera processor, 
the unaltered video stream and commands/feature maps sent by the orchestrator.

#### Video stream

The video stream is sent by the video forwarder. This video forwarder previously encoded the camera stream to HLS which is used by the camera processor.
Other input methods also exist, mainly image capture and video capture, although both are only used for benchmarking/testing purposes.
The HLS stream is wrapped together with the timestamp of the HLS segment so that time can be consistently tracked by both the camera processor and the interface, 
since both components utilize the same stream.
[processor/input README](processor/input/README.md)

#### Orchestrator

The orchestrator is the point of communication between both the camera processors and the interface.
The orchestrator is responsible for correctly distributing the data it gets.
The camera processors are responsible for sending the data required to re-identify a subject to all camera processors via the orchestrator.
The interface is responsible for choosing an object to track, which is done based on a previous output stage.

### Pipeline

The pipeline is responsible for processing all inputs, detecting all potential subject (detection of all objects), 
and tracking the subjects selected by the camera operator.
How these goals are achieved is explained in the [pipeline README](processor/pipeline/README.md).

### Output

There are two types of outputs:
detections possibly associated with a tracked subject, 
and re-identification data

#### Detections

All detections are shared with the interface to draw all trackable objects. 
Some detections might have an associated object ID, meaning these detections were already tracked.

#### Re-identification

All camera processors must be capable of finding the tracked subject. 
The processors need information about the subject to re-identify them.
This information is shared amongst processors.

## Running the application

The camera processor can be run both locally and in Docker although the used system must comply with the set requirements.
For differences in CUDA versions, check out the following [link](https://download.pytorch.org/whl/torch_stable.html) to see what distribution is available and choose one. We used the cu101 version because it was available for all of the members of the team.

### Environment variables
The following environment variables can be used:
(When these are set it overrides the configs.ini values with these)

| Variable         | Config.ini value name | Description                                                                 
| ---------------- | --------------------- | ----------------------------------------------------------------------------
| ORCHESTRATOR_URL | Orchestrator.url      | The link of the orchestrator websocket                                      
| HLS_STREAM_URL   | Input.hls_url         | The stream url of the video forwarder (when set it runs in Input.type "hls")
| PROCESSOR_MODE   | Main.mode             | In what mode the container runs                                             
| DETECTION_ALG    | Main.detector         | Name of the detection algorithm to use                                      
| TRACKING_ALG     | Main.tracker          | Name of the tracking algorithm to use                                       
| TRACKING_ALG     | Main.reid             | Name of the re-identification algorithm to use                              

### Configurations

CameraProcessor configurations inside the [configs.ini](configs.ini) file. Let's highlight some of the important ones:
- **Main.mode:** This is the mode in which the application runs
  - **deploy**: Connect using a WebSocket with the orchestrator URL
  - **opencv**: Display the resulting processed frames inside an OpenCV native window
  - **tornado**: Stream the processed frames to a web port
- **Input.type:** This is what type of input is used
  - **webcam**: Use the webcam_device_nr as camera
  - **images**: Goes through all images in order defined in Input.images_dir_path
  - **video**: Uses Input.video_file_path as the videofile
  - **hls**: Uses the Input.hls_url to create the HLS stream
- **Orchestrator.url:** Websocket url to connect to
- **weights_path**: Path to the weights file
- **conf-thres**: The threshold at which detection is counted
- **device**: What device does the algorithm need to run on
  - **cpu**
  - **0** for GPU
- **Filter.targets_path**: Link to the file containing which classes will get detected

### Running the app locally

Installing python dependencies:
Download [Python 3.8](https://www.python.org/downloads/release/python-3810/) 
and install the dependencies in [requirements.txt](requirements.txt) + [requirements-gpu.txt](requirements-gpu.txt).
```cmd
pip install -r requirements.txt
pip install -r requirements-gpu.txt
```

Then, if you have [cuDNN 7.6.5](https://developer.nvidia.com/rdp/cudnn-archive) (for which you have to join the
Windows Insider if using on windows) 
When [CUDA 10.1](https://developer.nvidia.com/cuda-10.1-download-archive-update2) is installed on your computer 
(once again, NVIDIA only), you should be able to locally run main.py in the processor directory.
This will be able to run the YOLOv5 detection algorithm.

### Running in Docker

If you want to be able to run it with GPU, it is a lot of hassle for Windows users and not recommended.
You need to get the Windows Insider program to use CUDA in WSL2.
Windows insider program slows down the speed of pc a lot. 

- GPU-enabled on Linux:
   1. You need an NVIDIA GPU that supports CUDA
   2. Check the version of the CUDA installation, change PyTorch import if needed
   3. Make sure the devices in configs.ini are set to 0
   4. Run ```docker-compose up``` in the root to build the container for deployment.
- GPU-enabled on windows (Not recommended):
   1. You need an NVIDIA GPU that supports CUDA
   2. Follow the [nvidia install guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) step-by-step to expose your GPU to the docker container.
   3. Make sure the devices in configs.ini are set to 0
   4. Run ```docker-compose up``` in the root to build the container for deployment.
   5. Check the logs of your docker container in Docker Desktop to see if it is working properly.
- GPU-disabled (can't run GPU code, only start container):
   1. In the configs.ini change the device value to CPU.
   2. Run ```docker-compose up``` in the root to build the container for deployment.

### Verifying in Docker

To verify the detection/tracking/re-identifying running inside Docker it is possible to stream to the localhost.
Add lines the following lines to the docker-compose.yml file inside the root inside the cameraprocessor service: 
```cmd
ports:
    - 9090:9090
```
Set the PROCESSOR_MODE environment variable to: "tornado".

Open the link printed in the console when running ```docker-compose up``` and the stream will get shown after a bit.

## Running the tests

We use Pytest for testing the code which makes it easy to see the coverage.
We can run the unit tests locally and inside Docker.
The integration tests can only be run without changing the code inside Docker.

For Docker, the setup and commands are already included inside the Dockerfile, these do not need any tweaking.
When running the tests locally inside PyCharm make sure the testing library has been set to Pytest for easy development.
Create a Pytest configuration in PyCharm and test the unit tests folder.

## Pylint with PyCharm

We use Pylint for python code quality assurance.

### Installation

Input following command terminal:
```
pip install pylint
```

Install the PyCharm plugin:

`Control+Alt+S` to open PyCharm settings.

Navigate to `Settings>Plugins`.

Search for `pylint`.

Install Pylint plugin.

#### Settings

`Control+Alt+S` to open PyCharm settings.

Navigate to `Settings>Other Settings>Pylint`.

Set up a link to Pylint and test settings.

Select the path to `.pylintrc` file (should be at the root of the project).

Click apply.

#### Live linting while developing

Navigate to `Edtior>Inspections>Pylint`

Check `Pylint real-time scan`

#### Ignoring folders from linting

Mark desired folder as Excluded in PyCharm (for local development).

Add folder name to `ignore=` in `pylintrc` (for CI pipeline).
