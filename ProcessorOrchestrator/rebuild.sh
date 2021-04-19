IMAGE_NAME="processor-orchestrator" 
CONTAINER_NAME="po-container" 

# Remove old container 
docker rm -f $CONTAINER_NAME 

# Create new image 
docker build --target=build -t $IMAGE_NAME .

# Remove dangling images 
docker image prune -f 

# Run new container ... 
docker run -p 80:80 --name $CONTAINER_NAME $IMAGE_NAME 
