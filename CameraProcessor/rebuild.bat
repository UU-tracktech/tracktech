<<<<<<< HEAD
set imageName=camera-processor
set containerName=camera-processor-container
=======
set imageName=camera-processor-yolov5
set containerName=camera-processor-yolov5-container
>>>>>>> develop

:: Remove old container
docker rm -f %containerName%

:: Create new image
docker build -t %imageName% .

:: Remove dangling images
docker image prune -f

:: Run new container...
<<<<<<< HEAD
docker run -t -d -p 9090:9090 --name %containerName% %imageName%
=======
docker run -t -d --gpus all --name %containerName% %imageName%
:: docker run -t -d --name %containerName% %imageName%

Pause
>>>>>>> develop
