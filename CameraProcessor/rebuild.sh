IMAGE_NAME="gpu-test" 
CONTAINER_NAME="gpu-container"

# Remove old container 
docker rm -f $CONTAINER_NAME

# Create new image 
docker build --target=deploy -t $IMAGE_NAME .

# Remove dangling images 
docker image prune -f 

# Run new container 
docker run -itd --gpus all --name $CONTAINER_NAME $IMAGE_NAME 
