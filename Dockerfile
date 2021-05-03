FROM python:3.8-slim-buster AS base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
ENV PYTHONPATH=/app
# ENV PYTHONPATH=/app/CameraProcessor

# Copy docs and install pip documentation requirements
COPY . .
RUN ["python3.8", "-m", "pip", "install", "-r", "docs/requirements.txt"]

# ENTRYPOINT ["python3.8", "docs/documentation.py", "-ci", "-rs", "CameraProcessor/processor", "ProcessorOrchestrator/src", "VideoForwarder/src"]