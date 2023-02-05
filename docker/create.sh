#!/bin/bash
CONTAINER_NAME=hex_game_sh
IMAGE_NAME="hex_game_sh_img"
TARGET_LAYER="final"

# BASE_IMAGE="ubuntu:focal"
# DOCKER_COMMAND="docker run"
BASE_IMAGE="nvidia/cudagl:11.4.2-devel"
DOCKER_COMMAND="docker run --gpus all"

user="user"
uid="1000"
gid="1000"

docker build -t $IMAGE_NAME \
  --build-arg base_image=$BASE_IMAGE \
  --build-arg file="./Dockerfile" \
  --build-arg ssh="default" \
  --build-arg target=$TARGET_LAYER \
  --build-arg user=$user \
  --build-arg uid=$uid \
  --build-arg gid=$gid .
 

exec $DOCKER_COMMAND \
     -it \
     --name $CONTAINER_NAME\
     --net=host \
     -e DISPLAY \
     --device=/dev/input \
     -e QT_X11_NO_MITSHM=1 \
     -v $HOME/.Xauthority:/home/$user/.Xauthority \
     -v "$HOME/hex_exchange:/home/$user/hex_exchange" \
     -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
     $IMAGE_NAME

# Remember to run this command on the host machine
# to allow the use of the display within the
# container for graphical applications: 
# $  sudo xhost +si:localuser:root

