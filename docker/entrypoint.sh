#!/bin/bash

. /opt/ros/${ROS_DISTRO}/setup.sh
. /uros_ws/install/setup.sh

. ~/px4_ros_com_ros2/install/setup.sh

if [ "$MICROROS_DISABLE_SHM" = "1" ] ; then
    if [ "$ROS_LOCALHOST_ONLY" = "1" ] ; then
        export FASTRTPS_DEFAULT_PROFILES_FILE=/tmp/disable_fastdds_shm_localhost_only.xml
    else
        export FASTRTPS_DEFAULT_PROFILES_FILE=/tmp/disable_fastdds_shm.xml
    fi
fi

exec ros2 run micro_ros_agent micro_ros_agent "$@"