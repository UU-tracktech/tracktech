# Docker Python project boilerplate
Steps to run docker image after installation

**inside powershell**
cd to CameraProcessor directory 

To build image yourself
```
docker-compose up
```
run code
```
docker run camera-processor
```

To pull from registry:
```
docker pull tracktech.ml:50007/camera-processor
```
run code
```
docker run tracktech.ml:50007/camera-processor 
``` 

Dependencies install
```
pip install -r requirements.txt
```

# Pylint with PyCharm

We use Pylint for python code quality assurance

## Installation:

Input following command terminal:
```
pip install pylint
```

Install the PyCharm plugin:

`Control+Alt+S` to open PyCharm settings

Navigate to `Settings>Plugins`

Search for `pylint`

Install Pylint plugin

### Settings:

`Control+Alt+S` to open PyCharm settings

Navigate to `Settings>Other Settings>Pylint`

Set up link to Pylint and test settings.

Select the path to pylintrc (should be at root of project)

Click apply.

### Ignoring folders from linting:

Mark desired folder as Excluded in PyCharm. (for local development)

Add folder name to `ignore=` in `pylintrc` (for CI pipeline)