set runservice=videoforwarder_video-forwarder-service
set testservice=videoforwarder_video-forwarder-testing-service

:: Create new image
docker build --target=testing -t %testservice% .
docker build --target=production -t %runservice% .

:: Remove dangling images
docker image prune -f

pause