set imageName=cameraprocessor
set containerName=cameraprocessorcontainer

:: Remove old container
docker rm -f %containerName%

:: Remove old image
docker image rm -f %imageName%

:: Create new image
docker build -t %imageName% .

:: Run new container, this one exposes port 8000
docker run -d -p 8000:8000 --name %containerName% %imageName%
pause