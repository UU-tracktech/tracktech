set imageName=tt-traefik-image
set containerName=tt-traefik-container

:: Remove old container
docker rm -f %containerName%

:: Remove old image
docker image rm %imageName%

:: Create new image
docker build -t %imageName% .

:: Run new container, this one exposes port 80 and 1935
docker run -d -p 50005:80 -p 50006:8080 --name %containerName% %imageName%