set imageName=video-forwarder
set containerName=video-forwarder-container

:: Remove old container
docker rm -f %containerName%

:: Create new image
docker build --target=testing -t %imageName% .

:: Remove dangling images
docker image prune -f

:: Run new container...
docker run  --env CONFIG_PATH="/NetworkConfig.json" --env STREAM_FOLDER="/streams" -t -d -p 80:80 --name %containerName% %imageName%

pause