IMAGE_NAME="camera-processor-yolov5" 
CONTAINER_NAME="camera-processor-yolov5-container"

# Remove old container 
docker rm -f $CONTAINER_NAME

# Create new image 
docker build --target=deploy -t $IMAGE_NAME .

# Remove dangling images 
docker image prune -f 

# Run new container 
docker run -t -d --gpus all --name $CONTAINER_NAME $IMAGE_NAME 
