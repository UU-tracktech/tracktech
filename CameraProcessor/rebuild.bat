set imageName=camera-processor
set containerName=camera-processor-container

:: Remove old container
docker rm -f %containerName%

:: Create new image
docker build -t %imageName% .

:: Remove dangling images
docker image prune -f

:: Run new container...
docker run -t -d -p 9090:9090 --name %containerName% %imageName%