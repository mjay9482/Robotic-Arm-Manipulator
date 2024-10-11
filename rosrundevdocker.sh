#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No arguments supplied! Assuming 'bash' as default."
    cmd="bash"
else
    cmd=$1
fi

# # Ensure the X11 socket directory exists
# mkdir -p /tmp/.X11-unix

docker run -it --rm --privileged --name manipulator_docker \
    --net=host \
    --env="DISPLAY" \
    --env="ROS_DOMAIN_ID=42" \
    --workdir="/home/Documents/Manipulator/" \
    --volume="$(pwd)":"/home/Documents/Manipulator/" \
    --volume="/dev/shm":"/dev/shm" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    mjay_docker:1.0 $cmd
