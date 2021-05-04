set imageName=tracktech-documentation
set containerName=tracktech-documentation-container

:: Remove old container
docker rm -f %containerName%

:: Create new image
docker build -t %imageName% .

:: Remove dangling images
docker image prune -f

:: Run new container...
docker run -t -d --name %containerName% %imageName% python3.8 docs/documentation.py -ci -rs CameraProcessor/processor
REM docker run -t -d --name %containerName% %imageName% python3.8 docs/documentation.py -ci -rs^
REM  utility docs^
REM  ProcessorOrchestrator/src ProcessorOrchestrator/testing^
REM  CameraProcessor/tests^
REM  VideoForwarder/src VideoForwarder/test^
REM  Interface/testingSelenium

REM CameraProcessor/processor

Pause
