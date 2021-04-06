# For more information, please refer to https://aka.ms/vscode-docker-python
# FROM tracktech.ml:50007/opencv-python:latest
FROM nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04

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
COPY src/pipeline/detection/yolov5/requirements.txt src/pipeline/detection/yolov5/requirements.txt
RUN ["python3.8", "-m", "pip", "install", "-r", "requirements.txt"]

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH=/app

# COPY webpage webpage
COPY configs.ini .
COPY coco.names .
COPY src src

WORKDIR src

CMD ["python3.8", "main.py"]

# https://developer.nvidia.com/cuda/wsl/download
