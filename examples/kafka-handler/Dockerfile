FROM python:3.8-slim-buster

## Pyton installation ##
RUN apt-get update && apt-get install -y git

## OpenCV 3.4 Installation ##
RUN apt-get install -y build-essential cmake  qt5-default libvtk6-dev zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev libopenexr-dev libgdal-dev \
    libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine2-dev \
    python-dev python-tk python-numpy python3-dev python3-tk python3-numpy unzip wget

# Install OpenCV for computer vision.
RUN wget https://github.com/opencv/opencv/archive/3.4.0.zip && unzip 3.4.0.zip && rm 3.4.0.zip && \
    cd opencv-3.4.0 && mkdir build && cd build && \
    cmake -DBUILD_EXAMPLES=OFF .. && \
    make -j4 && make install && rm -rf /opencv-3.4.0

## Install kafka-handler
RUN mkdir /kafka-handler
WORKDIR kafka-handler

# Adding python src files.
ADD index.py index.py
ADD mqueue.py mqueue.py
ADD requirements.txt requirements.txt

# Installing dependencies
RUN apt-get install python3-venv -y
RUN python3 -m venv kafka-handler
RUN kafka-handler/bin/pip install -r requirements.txt

# Run script from virtualenv.
CMD ["/kafka-handler/kafka-handler/bin/python", "index.py"]
