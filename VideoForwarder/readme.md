# build
```
docker build . -t "videoforwarding"
```

# run
use docker desktop or
```
docker run -d -p 80:8080 -p 1935:1935 "videoforwarding"
```

# send video (for testing)
```
ffmpeg -re -i {mp4 file path} -vcodec libx264 -vprofile baseline -g 30 -acodec aac -strict -2 -f flv rtmp://localhost/show/stream
```
or
```
ffmpeg -re -i {mp4 file path} -vcodec h264_nvenc -vprofile baseline -g 30 -acodec aac -strict -2 -f flv rtmp://localhost/show/stream
```
or
```
ffmpeg -list_devices true -f dshow -i dummy
ffmpeg -re -f dshow -i video={camera name}:audio={microphone name} -vcodec h264_nvenc -vprofile baseline -acodec aac -f flv -g 30 -strict -2 -f flv -pix_fmt yuv420p rtmp://localhost/show/stream
```



# receive video (for interface)
```
http://localhost/hls/stream.m3u8
```