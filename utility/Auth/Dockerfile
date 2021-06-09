FROM python:3.8-slim-buster AS lint

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set environment variables
WORKDIR /app
ENV PYTHONPATH=/app

# Install pylint
RUN ["pip", "install", "pylint==2.8.3"]

# Copy the files
COPY utility/Auth utility/Auth

WORKDIR /

ENTRYPOINT ["pylint","app","--rcfile=/app/.pylintrc"]