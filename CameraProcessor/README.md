# Docker Python project boilerplate
Steps to run docker image after installation

**inside powershell**
cd to CameraProcessor directory 

build image
```
docker-compose up
```
run code
```
docker run cameraprocessor
```
run tests
```
docker run cameraprocessor watch -t pytest -v
```
