# TrackTech: Real-time tracking of subjects and objects on multiple cameras

[![Forwarder Build](https://github.com/UU-tracktech/tracktech/actions/workflows/Forwarder_Build.yml/badge.svg)](https://github.com/UU-tracktech/tracktech/actions/workflows/Forwarder_Build.yml)
[![Interface Build](https://github.com/UU-tracktech/tracktech/actions/workflows/Interface_Build.yml/badge.svg)](https://github.com/UU-tracktech/tracktech/actions/workflows/Interface_Build.yml)
[![Orchestrator Build](https://github.com/UU-tracktech/tracktech/actions/workflows/Orchestrator_Build.yml/badge.svg)](https://github.com/UU-tracktech/tracktech/actions/workflows/Orchestrator_Build.yml)
[![Processor Build](https://github.com/UU-tracktech/tracktech/actions/workflows/Processor_Build.yml/badge.svg)](https://github.com/UU-tracktech/tracktech/actions/workflows/Processor_Build.yml)

[![Codecov](https://codecov.io/gh/UU-tracktech/tracktech/branch/develop/graph/badge.svg?token=swMWxrC43A)](https://codecov.io/gh/UU-tracktech/tracktech)

This project is part of the 2021 spring bachelor final project of the Bachelor of Computer Science at Utrecht University.
The team did this project at a request from ATOE, a part of the Dutch National Police.
The team that worked on the project consists of eleven students from the Bachelor of Computer Science and Bachelor of Game Technology.
This project has been done for educational purposes.
All code is open source, and proper credit is given to respective parties.

## Pylint

We use Pylint for python code quality assurance.

### Installation

Input following command terminal:

```
pip install pylint
```

### Gpu support

#### Updating/Installing drivers

Update your GPU drivers and restart the system for changes to take effect.
Optionally use a other driver listed after running `ubuntu-drivers devices`

```bash
sudo apt install nvidia-driver-460
sudo reboot
```

#### Installing the container toolkit

Add the distribution, update the package manager, install nvidia for docker, and restart docker for changes to take effect.
For more information look at the [install guide](https://docs.nvid ia.com/datacenter/cloud-native/container-toolkit/install-guide.html#install-guide)

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt update
sudo apt install -y nvidia-docker2
sudo systemctl restart docker
```

#### Acquire the gpu id

According to [this](https://gist.github.com/tomlankhorst/33da3c4b9edbde5c83fc1244f010815c) read the `GPU UUID` like GPU-a1b2c3d (just the first part) from

```bash
nvidia-smi -a
```

#### Add the resource

Add the `GPU UUID` from last step to the [Docker engine configuration file](https://docs.docker.com/config/daemon/#configure-the-docker-daemon) typically at `/etc/docker/daemon.json`. Create the file if it does not exist yet.

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

### Run

The Pylint linting should be run from the root with a specified Python module (sub system).
The command is as follows:

`pylint <Sub system> --rcfile=.pylintrc --reports=n`

`<Sub system>` is the Python module to run.
Pylint needs an `__init__.py` file in the root to parse all folders to lint.
This must be one of the sub systems since the root doesn't contain an `__init__.py` file.

`--rcfile` is the linting specification used by Pylint.

`--reports` sets whether the full report should be displayed or not.
Our recommendation would be `n` since this only displays linting errors/warnings, and the eventual score reached.

### Ignoring folders from linting

Some folders should be excluded from linting.
This could be for multiple reasons like,
the symlinked algorithms in camera processor,
the Python virtual environment folder, etc.
Add folder name to `ignore=` in `.pylintrc`.
