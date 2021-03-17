FROM python:3

# update repositories
RUN apt-get update

#Install ffmpeg
RUN apt install -y ffmpeg

# install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the source code
COPY streams streams
COPY src src

# Make sure port is available
EXPOSE 80

# Run server
ENTRYPOINT ["python"]
CMD ["/src/main.py"]
