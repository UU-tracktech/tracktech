# Base image for all camera processor components 
FROM python:3.8-slim-buster AS base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app 
ENV PYTHONPATH=/app

RUN apt update

RUN apt install -y ffmpeg

# Install pip requirements
COPY requirements.txt .
RUN ["python3.8", "-m", "pip", "install", "-r", "requirements.txt"]

FROM base AS test

COPY processor processor
COPY data/annotated/test data/annotated/test
COPY tests tests
COPY .coveragerc .coveragerc

FROM test AS lint

RUN ["python3.8", "-m", "pip", "install", "pylint"]
RUN ["python3.8", "-m", "pip", "install", "pylint-exit"]

RUN ["mkdir", "utility"]

WORKDIR /

FROM base as deploy 

# Graphic installation process
###########################################################################
# See https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/10.1/ubuntu18.04-x86_64/base/Dockerfile
# See https://sarus.readthedocs.io/en/stable/user/custom-cuda-images.html
###########################################################################
USER root

###########################################################################
# base
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates && \
    curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub | apt-key add - && \
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \
    echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list && \
    apt-get purge --autoremove -y curl \
    && rm -rf /var/lib/apt/lists/*

ENV CUDA_VERSION 10.1.243
ENV CUDA_PKG_VERSION 10-1=$CUDA_VERSION-1

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-cudart-$CUDA_PKG_VERSION \
    cuda-compat-10-1 \
    && ln -s cuda-10.1 /usr/local/cuda && \
    rm -rf /var/lib/apt/lists/*

# Required for nvidia-docker v1
RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64


###########################################################################
#runtime next
ENV NCCL_VERSION 2.7.8

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-$CUDA_PKG_VERSION \
    cuda-npp-$CUDA_PKG_VERSION \
    cuda-nvtx-$CUDA_PKG_VERSION \
    libcublas10=10.2.1.243-1 \
    libnccl2=$NCCL_VERSION-1+cuda10.1 \
    && apt-mark hold libnccl2 \
    && rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold libcublas10


###########################################################################
#cudnn7 (not cudnn8) next

ENV CUDNN_VERSION 7.6.5.32

RUN apt-get update && apt-get install -y --no-install-recommends \
    libcudnn7=$CUDNN_VERSION-1+cuda10.1 \
    && apt-mark hold libcudnn7 && \
    rm -rf /var/lib/apt/lists/*


ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES all
ENV NVIDIA_REQUIRE_CUDA "cuda>=10.1"



COPY requirements-gpu.txt requirements-gpu.txt
COPY processor/pipeline/detection/yolov5/requirements.txt processor/pipeline/detection/yolov5/requirements.txt
RUN ["python3.8", "-m", "pip", "install", "-r", "requirements-gpu.txt"]

COPY configs.ini .
COPY coco.names .

# docker build --target=deploy -t test-gpu:latest .

# docker run -itd --gpus all --name gpu-container test-gpu:latest
#  
# docker exec -it gpu-container bin/bash




# This does not seem to work well? 
# ENTRYPOINT ["python3.8", "-m", "pytest", "--cov-config=.coveragerc", "--cov=processor", "--cov-report", "html", "--cov-report", "term", "--junitxml=unit-report.xml tests/unittests"]


# FROM python:3.8-slim-buster as test

# # Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1

# # Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

# RUN apt update
# RUN apt install -y ffmpeg

# WORKDIR /app
# ENV PYTHONPATH=/app

# # Install pip requirements
# COPY requirements-test.txt .
# RUN ["python3.8", "-m", "pip", "install", "-r", "requirements-test.txt"]

# COPY data/annotated/test data/annotated/test
# COPY processor processor
# COPY tests tests
# COPY .coveragerc .coveragerc

# ENTRYPOINT ["python3.8", "-m", "pytest", "--cov-config=.coveragerc", "--cov=processor", "--cov-report", "html", "--cov-report", "term", "--junitxml=unit-report.xml", "tests/unittests"]

# FROM nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04 AS build

# RUN apt update
# RUN apt install -y ffmpeg
# RUN ["apt", "install", "-y", "python3.8"]
# RUN ["apt", "install", "-y", "python3-pip"]

# # Torch for this cuda version
# RUN ["python3.8", "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"]
# RUN ["python3.8", "-m", "pip", "install", "torch==1.8.0+cu101", "torchvision==0.9.0+cu101", "-f", "https://download.pytorch.org/whl/torch_stable.html"]

# WORKDIR /app

# # Install pip requirements
# COPY requirements.txt .
# COPY processor/pipeline/detection/yolov5/requirements.txt processor/pipeline/detection/yolov5/requirements.txt
# RUN ["python3.8", "-m", "pip", "install", "-r", "requirements.txt"]

# # Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1

# # Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

# ENV PYTHONPATH=/app

# # COPY webpage webpage
# COPY configs.ini .
# COPY coco.names .
# COPY processor processor

# WORKDIR /processor

# ENTRYPOINT ["python3.8", "main.py"]



# https://developer.nvidia.com/cuda/wsl/download
