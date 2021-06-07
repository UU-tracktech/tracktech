# tracktech: Real-time tracking of subjects and objects on multiple cameras

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
