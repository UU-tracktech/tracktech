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
FROM installer as test
WORKDIR /app

# Install python dependencies
COPY requirements-test.txt requirements-test.txt
RUN ["pip","install","--no-cache-dir","-r","requirements-test.txt"]

# Copy a test config
COPY NetworkConfig.json NetworkConfig.json

FROM test as test_unit
COPY tests/unittest tests
ENTRYPOINT ["pytest","--cov-config=.coveragerc","--cov-report","term","--cov-report","html","--cov=src/","--junitxml=vf-unit-report.xml","tests"]

FROM test as test_integration
COPY tests/integrationtest tests
ENTRYPOINT ["pytest", "--junitxml=vf-integration-report.xml", "tests"]


# Installation
FROM python:3.8-slim-buster as lint
WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pylint
RUN ["pip", "install", "pylint==2.6.0"]

RUN ["mkdir", "utility"]

# Copy the actual source code
COPY src src

ENTRYPOINT ["pylint","app","--rcfile=app/.pylintrc","--output-format=colorized"]


FROM installer AS testing
WORKDIR /app

# Copy a test config
COPY NetworkConfig.json NetworkConfig.json

# Make sure port is available
EXPOSE 80
EXPOSE 443

# Run server
ENTRYPOINT ["python","-u","src/main.py"]


FROM installer AS production
WORKDIR /app

# Make sure port is available
EXPOSE 80
EXPOSE 443

# Run server
ENTRYPOINT ["python","-u","src/main.py"]