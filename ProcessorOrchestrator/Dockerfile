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

WORKDIR /app
ENV PYTHONPATH=/app

# Install pip requirements
COPY requirements.txt .
RUN ["python3.8", "-m", "pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

RUN ["python3.8", "-m", "pip", "install", "pylint"]
RUN ["python3.8", "-m", "pip", "install", "pylint-exit"]

COPY src src 
COPY testing testing
COPY .coveragerc .coveragerc

RUN ["mkdir", "utility"]

WORKDIR /

EXPOSE 80
EXPOSE 443

