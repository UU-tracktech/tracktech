FROM python:3

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src src

# Make sure port is available
EXPOSE 8000

# Run server
ENTRYPOINT ["python"]
CMD ["/src/main.py"]