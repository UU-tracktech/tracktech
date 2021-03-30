FROM python:3-slim-buster

#Install ffmpeg
RUN apt update
RUN apt install -y ffmpeg

# install python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# create a streams folder
RUN ["mkdir","streams"]

# copy a test config
COPY NetworkConfig.json /NetworkConfig.json

# copy the source code
COPY src src

# Make sure port is available
EXPOSE 80
EXPOSE 443

# Run server
ENTRYPOINT ["python","-u","/src/main.py"]
