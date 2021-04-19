FROM python:3 AS build

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src src

# Make sure port is available
EXPOSE 80
EXPOSE 443

# Run server
ENTRYPOINT ["python","-u","/src/main.py"]

FROM python:3.8-slim-buster as testing

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt update

# Install pip requirements
COPY requirements-test.txt .
RUN ["python3.8", "-m", "pip", "install", "--no-cache-dir", "-r", "requirements-test.txt"]

RUN ["python3.8", "-m", "pip", "install", "pylint"]
RUN ["python3.8", "-m", "pip", "install", "pylint-exit"]

COPY src src
COPY testing testing
COPY .coveragerc .coveragerc

RUN ["mkdir", "utility"]

WORKDIR /

# Make sure port is available
EXPOSE 80
EXPOSE 443

# Run server
ENTRYPOINT ["pytest", "testing/unit_testing", "--cov-config=app/.coveragerc", "--cov=app/src", "--cov-report html", "--cov-report term", "--junitxml=po-unit-report.xml"]