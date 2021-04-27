FROM python:3 AS build

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY "Auth-1.0.tar.gz" "Auth-1.0.tar.gz"
RUN ["pip","install","Auth-1.0.tar.gz"]
COPY src src


FROM build AS testing

# Copy testing
COPY testing testing

# Run server
ENTRYPOINT ["pytest", "testing", "--junitxml=report.xml"]


FROM build as production

# Make sure port is available
EXPOSE 80
EXPOSE 443

# Run server
ENTRYPOINT ["python","-u","/src/main.py"]
