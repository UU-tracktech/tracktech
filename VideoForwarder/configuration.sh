#!/bin/bash
# config +urls

CONFIG="/usr/local/nginx/conf/nginx.conf"
> $CONFIG

echo "events {

}


# RTMP configuration
rtmp {
  server {
    # Print to log so we can see what happens
    access_log /dev/stdout;

    # Listen for incoming stream on standard RTMP port
    listen 1935;

    # Set the chunk size
    chunk_size 4000;

    application pull {
      # Live on
      live on;

      # Run this from start" >> $CONFIG

for i in $@
do
    ARR=(${i//;/ })
    echo "      exec_static /usr/bin/ffmpeg -i ${ARR[0]} -vcodec libx264 -c:a aac -f flv rtmp://localhost/live/${ARR[1]};" >> $CONFIG
done

echo "
     # disable consuming the stream from nginx as rtmp
      deny play all;
    }

    application live {
      live on;

      exec /usr/bin/ffmpeg -i rtmp://localhost/\$app/\$name -async 1 -vsync -1
        -c:v libx264 -c:a libvo_aacenc -b:v 128k -b:a 64k -vf \"scale=144:-2\" -tune zerolatency -preset veryfast -crf 23 -f flv rtmp://localhost/show/\$name_144p
        -c:v libx264 -c:a libvo_aacenc -b:v 768k -b:a 64k -vf \"scale=360:-2\" -tune zerolatency -preset veryfast -crf 23 -f flv rtmp://localhost/show/\$name_360p
        -c:v libx264 -c:a libvo_aacenc -b:v 1920k -b:a 64k -vf \"scale=720:-2\" -tune zerolatency -preset veryfast -crf 23 -f flv rtmp://localhost/show/\$name_720p;
    }

    application show {
      live on;
      hls on;

      # Where to stream the data to locally
      hls_path /mnt/hls/;

      # Amount of seconds per fragment
      hls_fragment 1;

      # Amount of seconds total for playlist
      hls_playlist_length 30;

      # Instruct clients to adjust resolution according to bandwidth
      hls_variant _144p BANDWIDTH=256000; # Very-Low bitrate, 144p resolution
      hls_variant _360p BANDWIDTH=1152000; # Medium bitrate, 360p resolution
      hls_variant _720p BANDWIDTH=4096000; # High bitrate, 720p resolution
    }
  }
}

http {
  sendfile off;
  tcp_nopush on;

  directio 512;
  default_type application/octet-stream;

  # Print to log so we can see what happens
  access_log /dev/stdout;
  error_log /dev/stdout;

  server {
    listen 8080;

    location / {
      # Disable cache
      add_header 'Cache-Control' 'no-cache';

      # CORS setup
      add_header 'Access-Control-Allow-Origin' '*' always;
      add_header 'Access-Control-Expose-Headers' 'Content-Length';

      # allow CORS preflight requests
      if (\$request_method = 'OPTIONS') {
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Max-Age' 1728000;
        add_header 'Content-Type' 'text/plain charset=UTF-8';
        add_header 'Content-Length' 0;
        return 204;
      }

      types {
        application/vnd.apple.mpegurl m3u8;
        video/mp2t ts;
      }

      root /mnt/;
    }
  }
}" >> $CONFIG

/usr/local/nginx/sbin/nginx -g "daemon off;"