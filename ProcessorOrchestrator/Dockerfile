FROM python:3

# install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make sure port is available
EXPOSE 8000

# Run server
CMD ["python", "/src/main.py"]