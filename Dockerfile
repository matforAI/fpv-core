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
    libgl1-mesa-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN rosdep init || true
RUN rosdep update

WORKDIR /ros_ws

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# ===============================
# AUTONOMOUS DRONE STACK
# ===============================

# MAVROS2
RUN apt update && apt install -y \
    ros-humble-mavros \
    ros-humble-mavros-extras \
    geographiclib-tools \
    && rm -rf /var/lib/apt/lists/*

RUN geographiclib-get-geoids egm96-5

# Nav2
RUN apt update && apt install -y \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    && rm -rf /var/lib/apt/lists/*

# Image pipeline
RUN apt update && apt install -y \
    ros-humble-image-pipeline \
    ros-humble-image-transport \
    ros-humble-camera-info-manager \
    && rm -rf /var/lib/apt/lists/*

