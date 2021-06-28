# Camera Processor

The job of the camera processor is to detect all potential subjects
and track the subjects that have been selected by the camera operators using the interface.
The camera operators only see the detections within a frame and the subjects they started tracking.
The tracking of subjects is performed over multiple cameras,
notifying the camera operator when a subject is re-identified.

## Quickstart

Run the following command to start the processor.

```bat
docker run -e HLS_STREAM_URL={Hls stream url} -e ORCHESTRATOR_URL={Orchestrator url} -e CAMERA_ID={Camera stream id} -e PROCESSOR_MODE=deploy -e DETECTION_ALG=yolov5 -e TRACKING_ALG=sort -e REID_ALG=torchreid tracktech/processor:latest
```

### Starting

The camera processor can be run both locally, and in Docker, although the used system must comply with the set requirements.
For differences in CUDA versions, check out the following
[link](https://download.pytorch.org/whl/torch_stable.html) to see what distribution is available and choose one.
CUDA 10.1 (version cu101) is used because it was available for all the members of the team.

#### Docker

If the system is to be run with GPU, it is much hassle for Windows users and not recommended.
In order to be able to run the system with GPU, access to the Windows Insider program is required to use CUDA in WSL2.
Windows insider program slows down the speed of pc a lot.

- GPU-enabled on Linux:
  1.  You need an NVIDIA GPU that supports CUDA.
  2.  Check the version of the CUDA installation, change PyTorch import if needed.
  3.  Make sure the devices in configs.ini are set to 0.
  4.  Run `docker-compose up` in the root to build the container for deployment.
- GPU-enabled on Windows (Not recommended):
  1.  a CUDA supported NVIDIA GPU is required.
  2.  Follow the [NVIDIA install guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) step-by-step to expose your GPU to the docker container.
  3.  Make sure the devices in configs.ini are set to 0.
  4.  Run `docker-compose up` in the root to build the container for deployment.
  5.  Check the docker container logs in Docker Desktop to see if it is working properly.
- GPU-disabled (cannot run GPU code, only start container):
  1.  In configs.ini, change the device value to CPU.
  2.  Run `docker-compose up` in the root to build the container for deployment.

#### Local

To run the system locally there are a few steps needed.

1. First install [all dependencies](#dependencies).
2. Open the CameraProcessor folder in an IDE.
3. Change the [configurations](###configurations).
4. Run main.py.

### Environment variables

The following environment variables can be used:
(When these are set, it overrides the configs.ini values with these)

| Variable         | Config.ini value name | Description                                                                  |
| ---------------- | --------------------- | ---------------------------------------------------------------------------- |
| ORCHESTRATOR_URL | orchestrator.url      | The link of the orchestrator websocket                                       |
| HLS_STREAM_URL   | Input.hls_url         | The stream URL of the video forwarder (when set it runs in Input.type "hls") |
| PROCESSOR_MODE   | Main.mode             | In what mode the container runs                                              |
| DETECTION_ALG    | Main.detector         | Name of the detection algorithm to use                                       |
| TRACKING_ALG     | Main.tracker          | Name of the tracking algorithm to use                                        |
| REID_ALG         | Main.reid             | Name of the re-identification algorithm to use                               |

### Configurations

CameraProcessor configurations inside the [configs.ini](configs.ini) file. Let's highlight some of the important ones:

- **Main.mode:** This is the mode in which the application runs.
  - **deploy**: Connect using a WebSocket with the orchestrator URL.
  - **opencv**: Display the resulting processed frames inside an OpenCV native window.
  - **tornado**: Stream the processed frames to a web port.
- **Input.type:** This is what type of input is used.
  - **webcam**: Use the webcam_device_nr as camera.
  - **images**: Goes through all images in order defined in Input.images_dir_path.
  - **video**: Uses Input.video_file_path as the video file.
  - **hls**: Uses the Input.hls_url to create the HLS stream.
- **Orchestrator.url:** Websocket url to connect to.
- **weights_path**: Path to the weights file.
- **conf-thres**: The threshold at which detection is counted.
- **device**: What device does the algorithm need to run on.
  - **cpu** (not recommended).
  - **0** for GPU.
- **Filter.targets_path**: Link to the file containing which classes will get detected, excluding detections with another found class.

### Configuration constraints

There are two configuration constraints due to the way re-identification works.
Feature maps generated by the camera processors can differ in size based on the used re-identification algorithm.
These feature maps are sent to the orchestrator, which shares them with the other camera processors.
This means that all camera processors must use the same re-identification algorithm,
and once a new algorithm is chosen all processors, and the orchestrator must be restarted.

- Restart orchestrator once re-identification algorithm is switched.
- Use the same re-identification algorithm across all processors.

## Architecture

The inner workings of the camera processor consist of three parts.
The input processed by the pipeline and sent to either other camera processors or the interface.

### Input

There are two inputs available to the camera processor,
the unaltered video stream and commands/feature maps sent by the orchestrator.

#### Video stream

The video forwarder sends the video stream.
This video forwarder previously encoded the camera stream to HLS, which the camera processor uses.
Other input methods also exist, mainly image capture and video capture,
although both are only used for benchmarking/testing purposes.
The HLS stream is wrapped together with the timestamp of the HLS segment
so that time can be consistently tracked by both the camera processor and the interface,
since both components utilize the same stream.

Further explanation is located in the [processor/input README](processor/input/README.md).

#### Orchestrator

The orchestrator is the point of communication between both the camera processors and the interface.
The orchestrator is responsible for correctly distributing the data it gets.
The camera processors are responsible for sending the data required to re-identify a subject to all camera processors via the orchestrator.
The interface is responsible for choosing an object to track, which is done based on a previous output stage.

### Pipeline

The pipeline is responsible for processing all inputs, detecting all potential subject (detection of all objects),
Furthermore, tracking the subjects selected by the camera operator.
How these goals are achieved is explained in the [pipeline README](processor/pipeline/README.md).

### Output

There are two types of outputs:
detections possibly associated with a tracked subject,
and re-identification data.

#### Detections

All detections are shared with the interface to draw all trackable objects.
Some detections might have an associated object ID, meaning the system already tracked these detections.

#### Re-identification

All camera processors must be capable of finding the tracked subject.
The processors need information about the subject to re-identify them.
The systems shares this information amongst processors.

## Dependencies

### Hardware

- [CUDA compatible NVIDIA GPU](https://developer.nvidia.com/cuda-gpus#compute): CUDA was used, which is not compatible with all GPUs. Only NVIDIA GPUs can support CUDA, and not every NVIDIA GPU supports CUDA.
- Min 4GB RAM.

### Software

The camera processor can be run both locally and in Docker, although the used system must comply with the set requirements.
For differences in CUDA versions, check out the following [link](https://download.pytorch.org/whl/torch_stable.html) to see what distribution is available and choose one. We used the cu101 version because it was available for all of the members of the team.

- [Python 3.8](https://www.python.org/downloads/release/python-3810/): no other Python versions have been tested.
- [CUDA 10.1.2](https://developer.nvidia.com/cuda-10.1-download-archive-update2): this CUDA version has been tested. _However, it has demonstrated to work with CUDA 11.1_
- [cuDNN 7.6.5](https://developer.nvidia.com/rdp/cudnn-archive): this cuDNN was chosen due to compatibility with CUDA 10.1.2.
- [FFmpeg](https://ffmpeg.org/download.html): This is to extract metadata from the HLS stream to synchronise the stream with the interface.

### Packages

Installing python dependencies:
Download [Python 3.8](https://www.python.org/downloads/release/python-3810/)
and install the dependencies in [requirements.txt](requirements.txt) + [requirements-gpu.txt](requirements-gpu.txt).

```cmd
pip install -r requirements.txt
pip install -r requirements-gpu.txt
pip install -r requirements-reid.txt
```

## Development

### Testing

We use [Pytest](https://docs.pytest.org/en/stable/index.html) to test the code, making it easy to see the coverage.

#### Docker

The setup and commands are already included inside the Dockerfile; these do not need any tweaking.
Running unit tests:

```
docker-compose -f compose/docker-compose_test_unit.yml up --build
```

Integration tests:

Then, if you have [cuDNN 7.6.5](https://developer.nvidia.com/rdp/cudnn-archive) (for which you have to join the
Windows Insider if using on windows)
When [CUDA 10.1](https://developer.nvidia.com/cuda-10.1-download-archive-update2) is installed on your computer
(once again, NVIDIA only), you should be able to run main.py in the processor directory locally.
This setup will be able to run the YOLOv5 detection algorithm.

### Verify application in Docker

In order to verify the detection/tracking/re-identifying running inside the Docker container, it is possible to stream the result to localhost.
Add the following lines to the docker-compose.yml file inside the root inside the camera processor service:

```cmd
ports:
    - 9090:9090
```

Set the PROCESSOR_MODE environment variable to "tornado".

Open the link printed in the console when running `docker-compose up` and the stream will get shown after a bit.

#### Local

When running the tests locally it is easiest to using the short command:

```cmd
pytest --cov-config=.coveragerc --cov-report term-missing --cov-report=term --cov=processor/ tests/unittests
```

Set the PROCESSOR_MODE environment variable to "tornado".

Open the link printed in the console when running `docker-compose up`, and the stream will get shown after a bit.

## Running the tests

We use Pytest for testing the code, which makes it easy to see the coverage.
We can run the unit tests locally and inside Docker.
The runners can only run the integration tests without changing the code inside Docker.

For Docker, the Dockerfile contains the setup and commands. These do not need any tweaking.
When running the tests locally inside PyCharm, ensure the testing library is set to Pytest for easy development.
Create a Pytest configuration in PyCharm and test the unit tests folder.

The final argument can be extended to test folders more specifically. This one runs the entire `unittest` folder.

To run integration tests locally, WebSocket URLs must be altered for the orchestrator or the HLS stream URL for the forwarder.
We strongly recommend using Docker to run these as described above.
