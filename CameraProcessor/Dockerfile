# Base image for all camera processor components 
FROM python:3.8-slim-buster AS test

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
COPY requirements-test.txt .
RUN ["pip", "install", "-r", "requirements.txt"]
RUN ["pip", "install", "-r", "requirements-test.txt"]

COPY data/tests data/tests
COPY data/videos data/videos
COPY pytest.ini pytest.ini
COPY configs.ini configs.ini
COPY test-configs.ini test-configs.ini
COPY .coveragerc .coveragerc
COPY processor processor
COPY coco.names coco.names
COPY tests/conftest.py tests/conftest.py


FROM test AS test_unit
COPY requirements-gpu.txt .
RUN ["pip", "install", "-r", "requirements-gpu.txt"]
COPY requirements-reid.txt .
RUN ["pip", "install", "-r", "requirements-reid.txt"]
COPY filter.names filter.names
COPY data/tests/unittests data/tests/unittests
COPY tests/unittests tests/unittests
ENTRYPOINT  ["pytest", "--cov-config=.coveragerc", "--cov-report", "term-missing", "--cov-report=term", "--cov-report=html", "--cov-report=xml", "--cov=processor/", "--junitxml=cp-unit-report.xml", "tests/unittests"]


FROM test as test_integration_forwarder
COPY tests/forwarderintegrationtests tests/forwarderintegrationtests
ENTRYPOINT  ["pytest", "tests/forwarderintegrationtests", "--cov=processor/", "--cov-config=.coveragerc", "--cov-report=xml", "--junitxml=cp-vf-integration-report.xml"]


FROM test as test_integration_orchestrator
COPY data/tests/integrationtests data/tests/integrationtests
COPY tests/orchestratorintegrationtests tests/orchestratorintegrationtests
ENTRYPOINT  ["pytest", "tests/orchestratorintegrationtests", "--cov=processor/", "--cov-config=.coveragerc", "--cov-report=xml", "--junitxml=cp-po-integration-report.xml"]


FROM test AS lint
RUN ["pip", "install", "pylint==2.8.2"]

COPY processor/ processor
COPY tests/ tests

RUN ["mkdir", "-p", "utility/pylint-plugins"]

WORKDIR /

ENTRYPOINT ["pylint", "app", "--rcfile=/app/.pylintrc"]


# Docker build that works with GPU on windows (with insider edition etc.) and linux
FROM nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04 AS deploy
WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# To enable the ability to use processor as a module
ENV PYTHONPATH=/app

RUN apt update
RUN ["apt", "install", "-y", "ffmpeg", "g++"]
RUN ["g++", "--version"]

RUN ["apt", "install", "-y", "python3.8", "python3.8-dev", "python3-pip"]
RUN ["python3.8", "-m", "pip", "install", "torch==1.8.0+cu101", "torchvision==0.9.0+cu101", "-f", "https://download.pytorch.org/whl/torch_stable.html"]

RUN ["python3.8", "-m", "pip", "install", "--upgrade", "pip"]

# Install pip requirements
COPY requirements.txt .
COPY requirements-gpu.txt .
COPY requirements-reid.txt .
COPY processor/pipeline/detection/yolov5/requirements.txt processor/pipeline/detection/yolov5/requirements.txt
COPY processor/pipeline/detection/yolor/requirements.txt processor/pipeline/detection/yolor/requirements.txt
COPY processor/pipeline/tracking/sort/requirements.txt processor/pipeline/tracking/sort/requirements.txt
COPY processor/pipeline/tracking/sort_oh/requirements.txt processor/pipeline/tracking/sort_oh/requirements.txt
COPY processor/pipeline/reidentification/torchreid/requirements.txt processor/pipeline/reidentification/torchreid/requirements.txt

RUN ["python3.8","-m","pip", "install", "-r", "requirements.txt"]
RUN ["python3.8","-m","pip", "install", "-r", "requirements-gpu.txt"]

# COPY webpage webpage
COPY configs.ini .
COPY filter.names .
COPY coco.names .
COPY data data
COPY webpage webpage
COPY processor processor

RUN ["python3.8","-m","pip", "install", "-r", "requirements-reid.txt"]

WORKDIR /processor

ENTRYPOINT ["python3.8", "/app/processor/main.py"]
