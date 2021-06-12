# Installation
FROM python:3.8-slim-buster as installer
WORKDIR /app
ENV PYTHONPATH=/app

# Install ffmpeg
RUN apt update
RUN apt install -y ffmpeg

# Create a streams folder
RUN ["mkdir","streams"]

# Install python dependencies
COPY "Auth-1.0.tar.gz" "Auth-1.0.tar.gz"
RUN ["pip","install","--no-cache-dir","Auth-1.0.tar.gz"]

COPY requirements.txt requirements.txt
RUN ["pip","install","--no-cache-dir","-r","requirements.txt"]

# Copy the actual source code
COPY src src


# testing container
FROM installer as test_unit
WORKDIR /app
COPY .coveragerc .
# Install python dependencies
COPY requirements-test.txt requirements-test.txt
RUN ["pip","install","--no-cache-dir","-r","requirements-test.txt"]

COPY tests/unittest tests

# Create multiple streams folders
RUN ["mkdir","streams1","streams2","streams3"]

ENTRYPOINT  ["bash","-c", "ffmpeg -f lavfi  -re -i testsrc -vcodec libx264 -listen 1 -profile:v baseline -pix_fmt yuv420p -f flv rtmp://localhost/stream & pytest --cov-config=.coveragerc --cov-report term --cov-report xml --cov-report term-missing --cov=src/ tests"]


# Installation
FROM python:3.8-slim-buster as lint
WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH=/app

# Install pylint
RUN ["pip", "install", "pylint==2.8.2"]

RUN ["mkdir", "utility"]

# Copy the actual source code
COPY src src
COPY tests tests

WORKDIR /

ENTRYPOINT ["pylint","app","--rcfile=/app/.pylintrc"]


FROM installer AS development
WORKDIR /app

# Make sure port is available
EXPOSE 80

# Run a test stream and the server
ENTRYPOINT ["bash","-c", "ffmpeg -f lavfi  -re -i testsrc -vcodec libx264 -listen 1 -profile:v baseline -pix_fmt yuv420p -f flv rtmp://localhost/stream & python -u src/main.py"]


FROM installer AS production
WORKDIR /app

# Make sure port is available
EXPOSE 80
EXPOSE 443

# Run server
ENTRYPOINT ["python","-u","src/main.py"]