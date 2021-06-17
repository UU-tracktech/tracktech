FROM python:3.8-slim-buster AS base

# Keeps Python from generating .pyc files in the container.
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging.
ENV PYTHONUNBUFFERED=1

# Set environment variables.
WORKDIR /app
ENV PYTHONPATH=/app

# Copy docs and install pip documentation requirements.
COPY docs/requirements.txt docs/requirements.txt
RUN ["python3.8", "-m", "pip", "install", "-r", "docs/requirements.txt"]

# Copy the rest of the application.
COPY . .

ENTRYPOINT ["python3.8", "docs/documentation.py", "-ci", "-rs", "utility", "docs", "CameraProcessor/processor", "ProcessorOrchestrator/src", "VideoForwarder/src"]