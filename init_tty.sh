#!/bin/bash

# doorbot tty init script
#
# install deps & do initial setup tasks
#   - download audio files & move to /data Volume
#   - /data only exists when container deployed to RPI
#		- must be run as sudo


################################################################################
# init - run once to setup new system

# binary dependancies
apt-get update \
	&& apt-get install -y \
		openssh-server \
    mosh \
		python \
		alsa-utils \
		libasound2-dev \
		mpg123 \
		flite \
		unzip \
		socat \
    unzip \
		fortunes fortune-mod \
	&& ln -s /usr/games/fortune /usr/local/bin \
	&& apt-get autoremove -y

# python dependancies
RUN python -m pip install pyserial boto3

# project directories
#
# $HOME is currently `/home/pi`
# manydoors repo lives in `/home/pi/rfid/access_control`
# tty src lives in `/home/pi/rfid/access_control`
# tty data lives in `/home/pi/rfid/access_control/tty`

if [ ! -d "$HOME/rfid" ]; then
  mkdir "$HOME/rfid/tty"; cd "$HOME/rfid/tty"
  if [ ! -d "$HOME/rfid/tty/themesongs" ]; then
    mkdir themesongs; cd themesongs
    wget -O songs.zip 'https://www.dropbox.com/sh/m502yddp4qr8til/AAAkaJgjKicYjvd8aTA-jQbqa?dl=1'
    unzip songs.zip; rm songs.zip   # unzip must be installed as above Dockerfile
    cd ..
  fi
  if [ ! -d "$HOME/rfid/tty/greetings" ]; then
    mkdir themesongs;
  fi
fi

# set the headphone jack volume to 99%
# currently amixer Volume control is numid=1
# NOTE: may need to double check this on new RPI hosts
#
# TODO: make sure this runs every reboot!
amixer controls | grep Volume | egrep --only-matching 'numid=[0-9]?' | xargs -I_ amixer cset _ 99%


################################################################################
# update - DL new themesongs; generate new greetings, delete old
#
#		call these functions (in greeting_tts.py) every day from access_conrol.py,
#		or via separate crontab entry?... thinking crontab...

# start access_control.py - take care of this with crontab
# python /app/access_control.py
