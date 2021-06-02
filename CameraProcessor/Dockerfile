# WSL docker build that works for windows
FROM nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04 AS wslbuild
WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

#
ENV PYTHONPATH=/app

RUN apt update
RUN ["apt","install","-y","ffmpeg","g++"]
RUN ["g++","--version"]

RUN ["apt","install","-y","python3.8", "python3.8-dev", "python3-pip"]
RUN ["python3.8","-m","pip", "install", "torch==1.8.0+cu101", "torchvision==0.9.0+cu101", "-f", "https://download.pytorch.org/whl/torch_stable.html"]

RUN ["python3.8","-m","pip", "install", "--upgrade", "pip"]

# Install pip requirements
COPY requirements.txt .
COPY requirements-gpu.txt .
COPY requirements-reid.txt .
COPY processor/pipeline/detection/yolov5/requirements.txt processor/pipeline/detection/yolov5/requirements.txt
COPY processor/pipeline/detection/yolor/requirements.txt processor/pipeline/detection/yolor/requirements.txt
COPY processor/pipeline/tracking/sort/requirements.txt processor/pipeline/tracking/sort/requirements.txt
COPY processor/pipeline/reidentification/torchreid/requirements.txt processor/pipeline/reidentification/torchreid/requirements.txt

RUN ["python3.8","-m","pip", "install", "-r", "requirements.txt"]
RUN ["python3.8","-m","pip", "install", "-r", "requirements-gpu.txt"]

# COPY webpage webpage
COPY configs.ini .
COPY filter.names .
COPY coco.names .
COPY processor processor
COPY data data

RUN ["python3.8","-m","pip", "install", "-r", "requirements-reid.txt"]

WORKDIR /processor

ENTRYPOINT ["python3.8", "/app/processor/main.py"]