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
#   consider following resin.io best-practices for checking
#     execution context https://resin.io/blog/where-is-my-code-running/
#   note: /data persists across container start/stop
if [ -d '/data' ]; then
  if [ ! -d '/data/music' ]; then
    mkdir /data/music; cd /data/music
    wget -O songs.zip 'https://www.dropbox.com/sh/m502yddp4qr8til/AAAkaJgjKicYjvd8aTA-jQbqa?dl=1'
    unzip songs.zip; rm songs.zip   # unzip installed via Dockerfile
  fi
fi

# set the headphone jack volume to 99%
# currently amixer Volume control is numid=1
amixer controls | grep Volume | egrep --only-matching 'numid=[0-9]?' | xargs -I_ amixer cset _ 99%

# start access_control.py
python /app/access_control.py
