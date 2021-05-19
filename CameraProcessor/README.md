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
For differences in CUDA versions, check out the following [link](https://download.pytorch.org/whl/torch_stable.html) to see what distribution is available and choose one. We used the cu101 version because it was available for all of the members in the team.

### Configurations

There are some configurations inside the [configs.ini](configs.ini) file. Lets highlight some of the important ones:
- **HLS.enabled:** When true the application will connect with the given url
- **Main.mode:** This is the mode in which the application runs
  - **deploy**: Connect using a websocket with the orchestrator url
  - **opencv**: Display the resulting processed frames inside an opencv native window
  - **tornado**: Stream the processed frames to a webport
- **Yolov5.source_path**: Path to the video file in case HLS is disabled
- **Yolov5.weights_path**: Path to the weights
- **Yolov5.conf-thres**: The threshold at which an detection is counted
- **Yolov5.device**: What the does yolov5 need to run on
  - **cpu**
  - **0** for gpu
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
   2. Check the version of the CUDA installation, change pytorch import if needed
   3. Make sure the Yolov5.device in configs.ini has value 0
   4. Run the docker-compose.yml in the root to build the container.
- GPU-enabled on windows (Not recommended):
   1. You need an NVIDIA GPU that supports CUDA
   2. Follow the [nvidia install guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) step-by-step to expose your GPU to the docker container.
   3. Make sure the Yolov5.device in configs.ini has value 0
   4. Run the docker-compose.yml in the root to build the container.
   5. Check the logs of your docker container in Docker Desktop to see if it is working properly.
- GPU-disabled (can't run GPU code, only start container):
   1. In the configs.ini change the device value to cpu.
   2. Run the docker-compose.yml in the root to build the container.

## Running the tests

We use pytest for testing the code which makes it easy to see the coverage.
We are able to run the unittests locally and inside Docker.
The integration tests can only be run without changing code inside Docker.

For Docker the setup and commands are already included inside the Dockerfile, these do not need any tweaking.
When running the tests locally inside PyCharm make sure the testing library has been set to pytest for easy development.
Create a pytest configuration in PyCharm and test the unittests folder.

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

Select the path to pylintrc (should be at the root of the project).

Click apply.

#### Live linting while developing

Navigate to `Edtior>Inspections>Pylint`

Check `Pylint real-time scan`

#### Ignoring folders from linting

Mark desired folder as Excluded in PyCharm (for local development).

Add folder name to `ignore=` in `pylintrc` (for CI pipeline).
