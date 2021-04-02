# For more information, please refer to https://aka.ms/vscode-docker-python
FROM tracktech.ml:50007/opencv-python:latest

EXPOSE 8000
EXPOSE 9090

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:/usr/app/src"

WORKDIR /app
COPY webpage webpage
COPY src src
COPY tests tests

EXPOSE 80
