#!/usr/bin/python
# Copyright 2016 Manylabs - MIT License
# Author: Mac Cowell
#
# Script that speaks (Amazon Polly tty | flite tty) a brief greeting, triggered
# by https://github.com/manylabs/manydoors RFID access system

import logging
import logging.handlers
import subprocess
from datetime import datetime

LOG_FILENAME = "/data/access_control.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#######################################################
# testing with ptmx pseudoterminal
    # see http://stackoverflow.com/questions/2174071/how-to-use-dev-ptmx-for-create-a-virtual-serial-port#15095316
    # can't figure out how to communicate (container issue? no tty...)
# use socat to create virtual serial ports; assuming 0, 1 file descriptors
    # simulate card read with (i hope):
    # `echo -ne '\x02entry:8905409\x03' > /dev/pts/1`
subprocess.Popen('socat pty,raw,echo=0 pty,raw,echo=0', shell=True)
time.sleep(5)
SERIAL_PORT = '/dev/pts/0'    # typically '/dev/pts/0'
#######################################################

idFile = "/app/ids.csv"             # wrong
accessLog = "/data/accessLog.csv"   # wrong

# def synthesizeFortunes( ):
    ```
    AWS Polly requests take 30s on the pi, so we generate & cache a bunch of new ones every day
    ```


# def synthesizeMotd( ):
    ```
    If there is a message of the day (motd) today, synthesize it
    ```


# def greetingPermutations ( name="unknow" ):
    ```
    constructs iterable list of entry & exit greeting strings for a given user
    name or genericly-addressed strings if no name given.
    ```


# def updateGreetings( ):
    ```
    synthesize permutations of entry & exit greetings for new users; delete files
    for removed users.
    ```

# rewrite; belongs in access_control.py
def playThemesong( msg ):

    # say hello/goodbye (TODO make blocking)
    subprocess.Popen("flite '" + msg + "'", shell=True)
    time.sleep(2)

    # select <name>.mp3 or default.mp3 if doesn't exist
    song = '/data/music/default.mp3'

    # if not already playing same song,
    # play themesong
    subprocess.Popen("mpg123 '" + song + "'", shell=True)

        # something like
        #   def play():
        #       subprocess.Popen("flite 'echo Hello World'", shell=True, stdout=subprocess.PIPE)
        #       subprocess.Popen("mpg123 /data/music/The_Final_Countdown_kazoo.mp3", shell=True, stdout=subprocess.PIPE)
        #
        # see executor
        #   https://executor.readthedocs.io/en/latest/#api-documentation
        # Popen deets
        #   https://jimmyg.org/blog/2009/working-with-python-subprocess.html

    # say inspirational message
