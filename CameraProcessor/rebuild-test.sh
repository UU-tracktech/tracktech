#!/bin/sh
IMAGE_NAME="camera-processor-test"
CONTAINER_NAME="camera-processor-test-container" 

# Remove old container
docker rm -f $CONTAINER_NAME 

# Create new image 
docker build --target=test -t $IMAGE_NAME .

# Remove dangling images 
docker image prune -f 

# Run new container 
docker run -t -d --name $CONTAINER_NAME $IMAGE_NAME


