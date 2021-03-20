set imageName=tt-forwarder-image
set containerName=tt-forwarder-container

:: Remove old container
docker rm -f %containerName%

:: Create new image
docker build -t %imageName% .

:: Remove dangling images
docker image prune -f

:: Run new container...
docker run -d -p 80:80 -p 443:443 --name %containerName% %imageName% /run/secrets/NetworkConfig.json
