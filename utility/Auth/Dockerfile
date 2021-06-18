FROM python:3.8-slim-buster AS lint

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set environment variables
WORKDIR /app
ENV PYTHONPATH=/app

# Install pylint
RUN ["pip", "install", "pylint==2.8.2"]

# Create an utility folder, to copy in the utility files.
RUN ["mkdir", "utility"]

# Copy the files
COPY auth auth

ENTRYPOINT ["pylint","auth","--rcfile=.pylintrc"]