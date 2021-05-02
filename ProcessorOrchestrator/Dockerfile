FROM python:3.8-slim-buster AS build

WORKDIR /
ENV PYTHONPATH=/

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY "Auth-1.0.tar.gz" "Auth-1.0.tar.gz"
RUN ["pip","install","Auth-1.0.tar.gz"]

COPY src src

# Make sure port is available
EXPOSE 80
EXPOSE 443

# Run server
ENTRYPOINT ["python","-u","/src/main.py"]

FROM python:3.8-slim-buster as testing

WORKDIR /
ENV PYTHONPATH=/

RUN apt update
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements-test.txt .
RUN ["python3.8", "-m", "pip", "install", "--no-cache-dir", "-r", "requirements-test.txt"]

COPY src src
COPY testing testing
COPY .coveragerc .coveragerc

RUN ["mkdir", "utility"]

WORKDIR /

# Make sure port is available
EXPOSE 80
EXPOSE 443

FROM testing as runtest

# Run server
ENTRYPOINT ["pytest", "testing/unit_testing", "--cov-config=.coveragerc", "--cov=src", "--cov-report=html", "--cov-report=xml", "--cov-report=term", "--junitxml=po-unit-report.xml"]
