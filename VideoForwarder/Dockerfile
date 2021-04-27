# Installation
FROM python:3.8-slim-buster as install

# Install python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Documentation container
FROM install as pdoc

# Install pdoc
RUN pip install pdoc

# Copy the source code
COPY src src

# Set src as the working directory
WORKDIR /src

# Make sure port is available
EXPOSE 8080

# Run pdoc
ENTRYPOINT ["pdoc","-h","0.0.0.0","main.py","camera.py","cameraHandler.py"]


# Production container
FROM install as testing

ENV SEGMENT_SIZE 2
ENV SEGMENT_AMOUNT 5
ENV CONFIG_PATH /NetworkConfig.json
ENV STREAM_FOLDER /streams
ENV ENCODING libx264

# Install ffmpeg
RUN apt update
RUN apt install -y ffmpeg

# Create a streams folder
RUN ["mkdir","streams"]

WORKDIR /

# Copy a test config
COPY NetworkConfig.json /NetworkConfig.json

# Copy the source code
COPY src src

# Copy integration and unit test code
COPY test test

# Make sure port is available
EXPOSE 80
EXPOSE 443

ENV PYTHONPATH=/

FROM testing AS production

# Run server
ENTRYPOINT ["python","-u","/src/main.py"]
