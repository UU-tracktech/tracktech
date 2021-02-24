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
docker run CameraProcessor
```
run tests
```
docker run CameraProcessor watch -t pytest -v
```
