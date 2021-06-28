# TrackTech: Real-time tracking of subjects and objects on multiple cameras

[![Forwarder Build](https://github.com/UU-tracktech/tracktech/actions/workflows/Forwarder_Build.yml/badge.svg)](https://github.com/UU-tracktech/tracktech/actions/workflows/Forwarder_Build.yml)
[![Interface Build](https://github.com/UU-tracktech/tracktech/actions/workflows/Interface_Build.yml/badge.svg)](https://github.com/UU-tracktech/tracktech/actions/workflows/Interface_Build.yml)
[![Orchestrator Build](https://github.com/UU-tracktech/tracktech/actions/workflows/Orchestrator_Build.yml/badge.svg)](https://github.com/UU-tracktech/tracktech/actions/workflows/Orchestrator_Build.yml)
[![Processor Build](https://github.com/UU-tracktech/tracktech/actions/workflows/Processor_Build.yml/badge.svg)](https://github.com/UU-tracktech/tracktech/actions/workflows/Processor_Build.yml)

[![Forwarder Docker Pulls](https://img.shields.io/docker/pulls/tracktech/forwarder?label=Forwarder%20Docker%20Pulls)](https://hub.docker.com/r/tracktech/forwarder)
[![Interface Docker Pulls](https://img.shields.io/docker/pulls/tracktech/interface?label=Interface%20Docker%20Pulls)](https://hub.docker.com/r/tracktech/interface)
[![Orchestrator Docker Pulls](https://img.shields.io/docker/pulls/tracktech/orchestrator?label=Orchestrator%20Docker%20Pulls)](https://hub.docker.com/r/tracktech/orchestrator)
[![Processor Docker Pulls](https://img.shields.io/docker/pulls/tracktech/processor?label=Processor%20Docker%20Pulls)](https://hub.docker.com/r/tracktech/processor)

[![Codecov](https://codecov.io/gh/UU-tracktech/tracktech/branch/develop/graph/badge.svg?token=swMWxrC43A)](https://codecov.io/gh/UU-tracktech/tracktech)

This project is part of the 2021 spring bachelor final project of the Bachelor of Computer Science at Utrecht University.
The team that worked on the project consists of eleven students from the Bachelor of Computer Science and Bachelor of Game Technology.
This project has been done for educational purposes.
All code is open-source, and proper credit is given to respective parties.

### GPU support

#### Updating/Installing drivers

Update the GPU drivers and restart the system for changes to take effect.
Optionally, use a different driver listed after running `ubuntu-drivers devices`

```bash
sudo apt install nvidia-driver-460
sudo reboot
```

#### Installing the container toolkit

Add the distribution, update the package manager, install NVIDIA for Docker, and restart Docker for changes to take effect.
For more information, look at the [install guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#install-guide)

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt update
sudo apt install -y nvidia-docker2
sudo systemctl restart docker
```

#### Acquire the GPU ID

According to [this](https://gist.github.com/tomlankhorst/33da3c4b9edbde5c83fc1244f010815c) read the `GPU UUID` like GPU-a1b2c3d (just the first part) from

```bash
nvidia-smi -a
```

#### Add the resource

Add the `GPU UUID` from the last step to the [Docker engine configuration file](https://docs.docker.com/config/daemon/#configure-the-docker-daemon) typically at `/etc/docker/daemon.json`. Create the file if it does not exist yet.

```json
{
  "runtimes": {
    "nvidia": {
      "path": "/usr/bin/nvidia-container-runtime",
      "runtimeArgs": []
    }
  },
  "default-runtime": "nvidia",
  "node-generic-resources": ["gpu=GPU-a1b2c3d"]
}
```

## Pylint

We use Pylint for python code quality assurance.

### Installation

Input following command terminal:

```
pip install pylint
```

### Run

To run linting on the entire repository run the following command from the root:
`pylint CameraProcessor docs Interface ProcessorOrchestrator utility VideoForwarder --rcfile=.pylintrc --reports=n`

#### Explanation
`pylint <Subsystem> --rcfile=.pylintrc --reports=n`

`<Subsystem>` is the Python module to run.

`--rcfile` is the linting specification used by Pylint.

`--reports` sets whether the full report should be displayed or not.
Our recommendation would be `n` since this only displays linting errors/warnings and the eventual score.

#### Constraints
Pylint needs an `__init__.py` file in the subsystem root to parse all folders to lint.
This run must be one of the subsystems since the root does not contain an `__init__.py` file.

### Ignoring folders from linting

Some folders should be excluded from linting.
The exclusion could be for multiple reasons like,
the symlinked algorithms in the CameraProcessor folder or
the Python virtual environment folder.
Add folder name to `ignore=` in `.pylintrc`.