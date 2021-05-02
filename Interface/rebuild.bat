set imageName=interface
set containerName=interface-container

:: Remove old container
docker rm -f %containerName%

:: Create new image
docker build -f Dockerfile_eslint -t %imageName% .

:: Remove dangling images
docker image prune -f

:: Run new container...
docker run -t -d --name %containerName% %imageName%
:: ./node_modules/.bin/eslint src/*.tsx src/*.ts

:: ENTRYPOINT ["./node_modules/.bin/eslint", "src/*.tsx", "src/*.ts"]

Pause