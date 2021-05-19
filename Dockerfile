FROM python:3.8-slim-buster AS base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
ENV PYTHONPATH=/app

# Copy docs and install pip documentation requirements
COPY . .
RUN ["python3.8", "-m", "pip", "install", "-r", "docs/requirements.txt"]

# ENTRYPOINT ["python3.8", "docs/documentation.py", "-ci", "-rs", "CameraProcessor/processor", "ProcessorOrchestrator/src", "VideoForwarder/src"]

#pages:
#  stage: deploy
#  before_script:
#    - docker build -t tracktech-documentation .
#    - docker rm -f tracktech-documentation-container || true
#  script:
#    - docker run --name tracktech-documentation-container tracktech-documentation python3.8 docs/documentation.py -ci -rs utility docs ProcessorOrchestrator/src ProcessorOrchestrator/testing CameraProcessor/tests VideoForwarder/src VideoForwarder/test Interface/testingSelenium
#    - docker cp tracktech-documentation-container:/app/docs/html/ public/
#  after_script:
#    - docker stop tracktech-documentation-container
#  artifacts:
#    when: always
#    paths:
#      - public
#    expire_in: 14 days