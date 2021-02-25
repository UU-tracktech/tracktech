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
ffmpeg -re -i {mp4 file path} -vcodec libx264 -vprofile baseline -g 30 -acodec aac -strict -2 -f flv rtmp://localhost:1935/show/stream
```
or
```
ffmpeg -re -i {mp4 file path} -vcodec h264_nvenc-vprofile baseline -g 30 -acodec aac -strict -2 -f flv rtmp://localhost:1935/show/stream
```


# receive video (for interface)
```
http://localhost/hls/stream.m3u8
```