set imageName=camera-processor
set containerName=camera-processor-test-container

:: Remove old container
docker rm -f %containerName%

:: Create new image
docker build --target=test -t %imageName% .

:: Remove dangling images
docker image prune -f

:: Run new container...
docker run -t -d --name %containerName% %imageName%

Pause