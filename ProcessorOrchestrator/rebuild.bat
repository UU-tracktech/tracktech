set imageName=processor-orchestrator
set containerName=po-container

:: Remove old container
docker rm -f %containerName%

:: Create new image
docker build -t %imageName% .

:: Remove dangling images
docker image prune -f

:: Run new container...
docker run -d -p 8000:8000 --name %containerName% %imageName%