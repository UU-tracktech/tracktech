FROM python:3 AS build

# install dependencies
COPY ProcessorOrchestrator/requirements.txt .
RUN pip install --no-cache-dir -r ProcessorOrchestrator/requirements.txt

COPY ProcessorOrchestrator/src src

# Make sure port is available
EXPOSE 80
EXPOSE 443

# Run server
ENTRYPOINT ["python","-u","/src/main.py"]

FROM python:3 AS testing

# install dependencies
COPY ProcessorOrchestrator/requirements.txt .
RUN pip install --no-cache-dir -r ProcessorOrchestrator/requirements.txt

COPY ProcessorOrchestrator/src src
COPY ProcessorOrchestrator/testing testing

COPY .pylintrc ../.pylintrc
COPY pylint_ignore.py pylint_ignore.py
COPY .coveragerc .coveragerc

# Make sure port is available
EXPOSE 80
EXPOSE 443

# Run server
# ENTRYPOINT ["pytest", "testing", "--junitxml=report.xml"]