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

### Running the app locally

Installing python dependencies:
Download [Python 3.8](https://www.python.org/downloads/release/python-3810/) 
and install the dependencies in [requirements.txt](requirements.txt).
```cmd
pip install -r requirements.txt
```

Then, if you have [cuDNN 7.6.5](https://developer.nvidia.com/rdp/cudnn-archive) (for which you have to join the
membership) 
for [CUDA 10.1](https://developer.nvidia.com/cuda-10.1-download-archive-update2) installed on your computer 
(once again, NVIDIA only), you should be able to locally run main.py in the src directory.
This will run the YOLOv5 detection algorithm.


Dependencies install
```
pip install -r requirements-gpu.txt
```

### Running in Docker

If you want to be able to run it with GPU, it is a lot of hassle for Windows users and not recommended.
You need to get the Windows Insider program to use CUDA in WSL2.
Windows insider program slows down the speed of pc a lot. 

1. GPU-enabled (Not recommended):
   1. You need an NVIDIA GPU that supports CUDA
   2. Follow the [nvidia install guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) step-by-step to expose your GPU to the docker container.
   3. Run rebuild.bat to build the container.
   4. Check the logs of your docker container in Docker Desktop to see if it is working properly.
2. GPU-disabled (can't run GPU code, only start container):
   1. Comment out the line ```CMD ["python3.8", "main.py"]``` in the Dockerfile.
   2. Replace the line ```docker run -t -d --gpus all --name %containerName% %imageName%``` by 
   ```docker run -t -d --name %containerName% %imageName%``` in the rebuild.bat file and run it.
   3. Now, you should be able to at least start the container. You will not be able to run any code, however.
   
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
