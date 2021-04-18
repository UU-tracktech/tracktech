# Installation
FROM python:3-slim-buster as install

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
FROM install as production

# Install ffmpeg
RUN apt update
RUN apt install -y ffmpeg

# Create a streams folder
RUN ["mkdir","streams"]

# Copy a test config
COPY NetworkConfig.json /NetworkConfig.json

# Copy the source code
COPY src src

# Make sure port is available
EXPOSE 80
EXPOSE 443

# Run server
ENTRYPOINT ["python","-u","/src/main.py"]
