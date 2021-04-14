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

FROM python:3 AS testing

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src src
COPY testing testing

# Make sure port is available
EXPOSE 80
EXPOSE 443

# Run server
ENTRYPOINT ["pytest", "testing", "--junitxml=report.xml"]

FROM python:3 AS linting

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

#RUN apt update
#RUN apt install -y ffmpeg

WORKDIR /app
ENV PYTHONPATH=/app

# Install pip requirements
COPY requirements.txt .
RUN ["python3", "-m", "pip", "install", "--no-cache-dir", "-r", "requirements.txt"]
RUN ["python3", "-m", "pip", "install", "pylint"]
RUN ["python3", "-m", "pip", "install", "pylint-exit"]

COPY src src
COPY testing testing

WORKDIR /

COPY .pylintrc ../.pylintrc
COPY pylint_ignore.py pylint_ignore.py