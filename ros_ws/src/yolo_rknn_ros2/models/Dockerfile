FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    nano \
    vim \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-vcstool \
    libopencv-dev \
    libeigen3-dev \
    libpangolin-dev \
    libyaml-cpp-dev \
    libboost-all-dev \
    libglew-dev \
    libgl1 \
    libglib2.0-0 \
    libgtk-3-dev \
 && rm -rf /var/lib/apt/lists/*

RUN rosdep init || true
RUN rosdep update

WORKDIR /ros_ws
