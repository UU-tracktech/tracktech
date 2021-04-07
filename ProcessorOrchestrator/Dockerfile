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
ENTRYPOINT ["pytest", "testing"]