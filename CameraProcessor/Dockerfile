FROM python:3.8-slim-buster as test

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt update
RUN apt install -y ffmpeg

WORKDIR /app
ENV PYTHONPATH=/app

# Install pip requirements
COPY requirements-test.txt .
RUN ["python3.8", "-m", "pip", "install", "-r", "requirements-test.txt"]
RUN ["python3.8", "-m", "pip", "install", "pylint"]
RUN ["python3.8", "-m", "pip", "install", "pylint-exit"]

COPY data/annotated/test data/annotated/test
COPY processor processor
COPY tests tests

WORKDIR /


COPY ../.pylintrc .pylintrc
COPY ../utils/pylint_ignore.py utils/pylint_ignore.py
COPY .coveragerc .coveragerc


FROM nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04 AS build

RUN apt update
RUN apt install -y ffmpeg
RUN ["apt", "install", "-y", "python3.8"]
RUN ["apt", "install", "-y", "python3-pip"]

# Torch for this cuda version
RUN ["python3.8", "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"]
RUN ["python3.8", "-m", "pip", "install", "torch==1.8.0+cu101", "torchvision==0.9.0+cu101", "-f", "https://download.pytorch.org/whl/torch_stable.html"]

WORKDIR /app

# Install pip requirements
COPY requirements.txt .
COPY processor/pipeline/detection/yolov5/requirements.txt processor/pipeline/detection/yolov5/requirements.txt
RUN ["python3.8", "-m", "pip", "install", "-r", "requirements.txt"]

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH=/app

# COPY webpage webpage
COPY configs.ini .
COPY coco.names .
COPY processor processor

WORKDIR /processor

ENTRYPOINT ["python3.8", "main.py"]



# https://developer.nvidia.com/cuda/wsl/download
