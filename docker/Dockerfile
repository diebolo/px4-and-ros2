# Build arguments
ARG ROS_DISTRO=humble

# Base image
FROM ros:${ROS_DISTRO}-ros-base

RUN apt-get update && apt-get upgrade -y
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv pip install ADS1x15-ADC --system

# Set up micro-dds-agent
RUN mkdir -p /px4_uros_uxrce_dds_ws/src
RUN git clone https://github.com/eProsima/Micro-XRCE-DDS-Agent.git -b v2.4.2 /px4_uros_uxrce_dds_ws/src/micro-xrce-dds-agent
RUN cd /px4_uros_uxrce_dds_ws && . /opt/ros/${ROS_DISTRO}/setup.sh && colcon build --packages-select microxrcedds_agent

RUN git clone https://github.com/diebolo/px4-and-ros2 /px4_uros_uxrce_dds_ws/src/angle_publisher
RUN cd /px4_uros_uxrce_dds_ws && . install/setup.sh && colcon build --packages-select angle_publisher


# Source ROS2 and the local workspace
RUN echo ". /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc
RUN echo ". ~/px4_uros_uxrce_dds_ws/install/setup.bash" >> ~/.bashrc

# Add the entrypoint script
ADD ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/bin/sh", "/entrypoint.sh" ]
CMD ["--help"]


