# For more information, please refer to https://aka.ms/vscode-docker-python
# FROM tracktech.ml:50007/opencv-python:latest
FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04

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
RUN ["python3.8", "-m", "pip", "install", "-r", "requirements.txt"]

EXPOSE 9090

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH="$PYTHONPATH:/usr/app/src"

RUN ["python3.8", "-m", "pip", "install", "absl-py"]
RUN ["python3.8", "-m", "pip", "install", "requests"]
RUN ["python3.8", "-m", "pip", "install", "opencv-python-headless"] 

# COPY webpage webpage
COPY configs.ini .
COPY coco.names .
COPY src src

# https://developer.nvidia.com/cuda/wsl/download

# ENV DEBIAN_FRONTEND noninteractive

# RUN ["apt", "remove", "-y", "nvidia-384"]
# RUN ["apt", "install", "-y", "nvidia-384"]
# COPY tests tests
