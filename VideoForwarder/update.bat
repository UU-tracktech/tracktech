set imageName=videoforwarderimage
set containerName=videoforwardercontainer

:: Remove old container
docker rm -f %containerName%

:: Remove old image
docker image rm %imageName%

:: Create new image
docker build -t %imageName% .

:: Run new container, this one exposes port 80 and 1935
docker run -d -p 80:8080 -p 1935:1935 --name %containerName% %imageName%