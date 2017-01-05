#!/bin/bash

# doorbot dockerfile init script
#
# do initial setup tasks just once per build
#   - download audio files & move to /data Volume
#   - /data only exists when container deployed to RPI
#
# then start doorbot python script

# if /data exists we are executing on RPI
# if /data/music doesn't exist this is fresh deploy
#   note: /data persists across container start/stop
if [ -d '/data' ]; then
  if [ ! -d '/data/music' ]; then
    mkdir /data/music; cd /data/music
    wget -O songs.zip 'https://www.dropbox.com/sh/m502yddp4qr8til/AAAkaJgjKicYjvd8aTA-jQbqa?dl=1'
    unzip songs.zip; rm songs.zip   # unzip installed via Dockerfile
  fi
fi

# start access_control.py
python /home/pi/rfid/access_control/access_control.py
