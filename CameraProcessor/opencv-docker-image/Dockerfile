# Docker image containing Python 3.8 bounded to OpenCV 4.5.1 with extra modules 

# https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html
# https://linuxize.com/post/how-to-install-opencv-on-debian-10/
# For more information, please refer to https://aka.ms/vscode-docker-python

# Pull from debian base image
FROM python:3.7-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN python -m pip install "numpy==1.19.5"

# Install OpenCV 
RUN apt-get update \ 
    && apt-get -y install build-essential cmake wget unzip pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev \
    libtbb2 libtbb-dev libdc1394-22-dev \
    && mkdir ~/opencv_build && cd ~/opencv_build \ 
    && wget -O opencv.zip https://github.com/opencv/opencv/archive/4.5.1.zip \
    &&  wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.1.zip \
    && unzip -q opencv.zip \
    && unzip -q opencv_contrib.zip \
    && cd ~/opencv_build/opencv-4.5.1 \ 
    && mkdir build && cd build \ 
    && cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib-4.5.1/modules \
    -D OPENCV_ENABLE_NONFREE=ON \
    # Extra build (like GPU support) options can be added below 
    .. \
    && make -j$(nproc) \ 
    && make install \ 
    # Clean up image 
    && cd ~ \
    && rm -rf opencv_build \ 
    && apt-get purge -y build-essential cmake wget unzip \ 
    && apt-get autoremove -y --purge 

