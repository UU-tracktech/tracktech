# Base image for all camera processor components 
FROM python:3.8-slim-buster AS base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app 
ENV PYTHONPATH=/app

RUN ["pip", "install", "torch==1.8.0+cu101", "torchvision==0.9.0+cu101", "-f", "https://download.pytorch.org/whl/torch_stable.html"]

RUN apt update

RUN apt install -y ffmpeg
RUN apt install -y g++

# Install pip requirements
COPY requirements.txt .
RUN ["pip", "install", "-r", "requirements.txt"]


FROM base AS test

COPY data/annotated/test data/annotated/test
COPY data/videos data/videos
COPY pytest.ini pytest.ini
COPY configs.ini configs.ini
COPY .coveragerc .coveragerc
COPY processor processor
COPY tests/conftest.py tests/conftest.py


FROM test AS test_unit
COPY requirements-gpu.txt .
RUN ["pip", "install", "-r", "requirements-gpu.txt"]
COPY filter.names filter.names
COPY data/tests/unittests data/tests/unittests
COPY tests/unittests tests/unittests
ENTRYPOINT  ["pytest","--cov-config=.coveragerc","--cov-report","term","--cov-report","html","--cov=processor/","--junitxml=cp-unit-report.xml","tests/unittests"]


FROM test as test_integration_forwarder
COPY tests/forwarderintegrationtests tests/forwarderintegrationtests
ENTRYPOINT  ["pytest","tests/forwarderintegrationtests" ,"--junitxml=cp-vf-integration-report.xml"]


FROM test as test_integration_orchestrator
COPY data/tests/integrationtests data/tests/integrationtests
COPY tests/orchestratorintegrationtests tests/orchestratorintegrationtests
ENTRYPOINT  ["pytest", "tests/orchestratorintegrationtests" ,"--junitxml=cp-po-integration-report.xml"]


FROM test AS lint
RUN ["pip", "install", "pylint==2.6.0", "pylint-exit"]

RUN ["mkdir", "utility"]

WORKDIR /
COPY data data
COPY tests tests

ENTRYPOINT ["pylint","app","--rcfile=app/.pylintrc","--output-format=colorized"]


FROM base as deploy 

# https://stackoverflow.com/a/64422438
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
#cudnn7 next

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
COPY processor/pipeline/tracking/sort/requirements.txt processor/pipeline/tracking/sort/requirements.txt
RUN ["pip", "install", "-r", "requirements-gpu.txt"]

COPY configs.ini .
COPY coco.names .
COPY processor processor 

WORKDIR /app/processor


# WSL docker build that works for windows
FROM nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04 AS wslbuild

RUN apt update
RUN apt install -y ffmpeg
RUN ["apt", "install", "-y", "python3.8", "python3-pip"]

WORKDIR /app

# Install pip requirements
COPY requirements.txt .
COPY requirements-gpu.txt .
COPY processor/pipeline/detection/yolov5/requirements.txt processor/pipeline/detection/yolov5/requirements.txt
RUN ["pip", "install", "-r", "requirements.txt", "requirements-gpu.txt"]

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH=/app

# COPY webpage webpage
COPY configs.ini .
COPY coco.names .
COPY processor processor
COPY data data

WORKDIR /processor

ENTRYPOINT ["python3.8", "main.py"]

# Run python3.8 main.py

# docker build --target=deploy -t test-gpu:latest .
#
# docker run -itd --gpus all --name gpu-container test-gpu:latest
#
# docker exec -it gpu-container bin/bash
