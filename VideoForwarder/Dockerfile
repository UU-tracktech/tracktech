# Installation
FROM python:3.8-slim-buster as install

# Install python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY "Auth-1.0.tar.gz" "Auth-1.0.tar.gz"
RUN ["pip","install","Auth-1.0.tar.gz"]


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

# Install ffmpeg and curl
RUN apt update
RUN apt install -y ffmpeg
RUN apt install -y curl

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
