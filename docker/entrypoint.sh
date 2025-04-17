#!/bin/bash

# Source ROS environment
. /opt/ros/${ROS_DISTRO}/setup.sh
# Source your workspace environment
. /px4_uros_uxrce_dds_ws/install/setup.sh

# Define a cleanup function
cleanup() {
    echo "Caught signal, stopping processes..."
    # Kill the agent and ROS2 node
    kill -TERM $AGENT_PID $ROS2_PID 2>/dev/null
    wait $AGENT_PID $ROS2_PID 2>/dev/null
    echo "Exiting cleanly"
    exit 0
}

# Set trap for SIGINT (Ctrl+C) and SIGTERM
trap cleanup SIGINT SIGTERM

# Run the MicroXRCEAgent with passed arguments
MicroXRCEAgent "$@" &
AGENT_PID=$!

# Run your ROS2 node
ros2 run angle_publisher angle_publisher &
ROS2_PID=$!

# Wait for both processes to exit
wait $AGENT_PID $ROS2_PID

# If we get here, one of the processes exited on its own
echo "A process has exited. Cleaning up..."
cleanup