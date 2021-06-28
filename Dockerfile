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

COPY Interface/react/package.json package.json

# Install nodejs, to use npm
RUN ["apt","update"]
RUN ["apt","install","-y","nodejs", "npm"]

RUN ["npm", "install"]

COPY Interface/react/src Interface/react/src
COPY Interface/react/tsconfig.json Interface/react/tsconfig.json

RUN ["npx", "typedoc", "--out", "docs/html/Interface", "Interface/react/src", "--tsconfig", "Interface/react/tsconfig.json", "--theme", "Interface/react/node_modules/typedoc-dark-theme/bin/default/"]


# Copy the rest of the application.
COPY . .

ENTRYPOINT ["python3.8", "docs/documentation.py", "-ci", "-rs", "utility", "docs", "CameraProcessor/processor", "ProcessorOrchestrator/src", "VideoForwarder/src"]