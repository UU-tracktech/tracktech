FROM debian:buster-slim

#https://dzone.com/articles/clone-code-into-containers-how
#Update the package manager
RUN apt-get update

#Install git
RUN apt-get install -y git

#Install wget
RUN apt-get install -y wget

#Install ffmpeg
RUN apt install -y ffmpeg

#https://docs.peer5.com/guides/setting-up-hls-live-streaming-server-using-nginx/
#Clone nginx-rtmp-module
RUN git clone https://github.com/sergey-dryabzhinsky/nginx-rtmp-module.git

#Install nginx dependencies
RUN apt-get install -y build-essential libpcre3 libpcre3-dev libssl-dev

#Download nginx
RUN wget http://nginx.org/download/nginx-1.18.0.tar.gz

#Open the tar.gz
RUN tar -xf nginx-1.18.0.tar.gz

#Compile nginx
RUN cd nginx-1.18.0 && ./configure --add-module=/nginx-rtmp-module --without-http_gzip_module && \
  make && \
  make install

#Copy static files into the image
COPY configuration.sh /configuration.sh

#Make sure port 8080 can be reached (to request data)
EXPOSE 8080

#Make sure port 1935 can be reached (to deliver data)
EXPOSE 1935

#Make sure the console stuff goes to the right place and the daemon doesn't keep secrets
ENTRYPOINT ["./configuration.sh"]
CMD ["rtsp://root:root@192.168.178.30/axis-media/media.amp;cam1"]