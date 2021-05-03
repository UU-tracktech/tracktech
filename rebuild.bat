set imageName=tracktech-documentation
set containerName=tracktech-documentation-container

:: Remove old container
docker rm -f %containerName%

:: Create new image
docker build -t %imageName% .

:: Remove dangling images
docker image prune -f

:: Run new container...
:: docker run -t -d --name %containerName% %imageName%
docker run -t -d --name %containerName% %imageName% python3.8 docs/documentation.py -ci -rs^
 utility^
 CameraProcessor/tests^
 ProcessorOrchestrator/src
:: CameraProcessor Interface ProcessorOrchestrator VideoForwarder
:: CameraProcessor/tests ProcessorOrchestrator/src VideoForwarder/src
REM
REM !docs
REM !utility
REM
REM !CameraProcessor/processor
REM !CameraProcessor/tests
REM
REM !Interface/testingSelenium
REM
REM !ProcessorOrchestrator/src
REM !ProcessorOrchestrator/testing
REM
REM !VideoForwarder/src
REM !VideoForwarder/test

Pause
