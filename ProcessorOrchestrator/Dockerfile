FROM python:3.8-slim-buster as test
WORKDIR /app
ENV PYTHONPATH=/app

RUN apt update
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements-test.txt .
RUN ["python3.8", "-m", "pip", "install", "--no-cache-dir", "-r", "requirements-test.txt"]

COPY "Auth-1.0.tar.gz" "Auth-1.0.tar.gz"
RUN ["pip","install","Auth-1.0.tar.gz"]

COPY src src
COPY tests tests
COPY .coveragerc .coveragerc

RUN ["mkdir", "utility"]

# Make sure port is available
EXPOSE 80
EXPOSE 443


FROM test as test_unit
ENTRYPOINT ["pytest","tests/unit_testing","--cov-config=.coveragerc","--cov=src","--cov-report=html","--cov-report=xml","--cov-report=term","--junitxml=po-unit-report.xml"]


FROM test as test_integration


FROM test as lint
WORKDIR /app
ENTRYPOINT ["pylint","src","tests","--rcfile=.pylintrc","--output-format=colorized"]


FROM python:3.8-slim-buster AS build
WORKDIR /app
ENV PYTHONPATH=/app

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
ENTRYPOINT ["python","-u","src/main.py"]