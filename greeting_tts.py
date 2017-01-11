#!/usr/bin/python
# Copyright 2016 Manylabs - MIT License
# Author: Mac Cowell
#
# Script that speaks (Amazon Polly tty | flite tty) a brief greeting, triggered
# by https://github.com/manylabs/manydoors RFID access system

import os
import logging
import logging.handlers
import subprocess
import boto3
from datetime import datetime

# rootdir = '/home/pi/rfid/access_control/'
rootdir = ''	# DEVELOPMENT

LOG_FILENAME = rootdir + 'access_control.log'
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

# subprocess.Popen('socat pty,raw,echo=0 pty,raw,echo=0', shell=True)
# time.sleep(5)
# SERIAL_PORT = '/dev/pts/0'    # typically '/dev/pts/0'
#######################################################

idFile = rootdir + 'ids.csv'
accessLog = rootdir + 'accessLog.csv'
tty_dir = rootdir + 'tty/'

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
            print("mkdir " + dir)
            os.makedirs(dir)

def find_name(name):
    # 'unknown' always exists
    if name == 'unknown': return True

    with open(idFile, 'r', os.O_NONBLOCK) as f:
        for line in f:
            # Ignore blank and commented lines
            if line and not line.startswith("#"):

            # Separate values
                cardId, valid_name = [v.strip().lstrip("0") for v in line.split(",")]
                if valid_name == name: return True

    return False    # name not found

def find_names(*names):
    if len(names) > 10000:  # be nice
        print("greetings_tts.py:find_names(*names) called with too many names (>10000)")
        return False

    # 'Unknown' is the only allowed default name
    valid_names = ['Unknown']
    if len(names) is 1 and names[0] == 'Unknown': return True

    # parse the list of valid names
    with open(idFile, 'r', os.O_NONBLOCK) as f:
        for line in f:
            # Ignore blank and commented lines
            if line and not line.startswith("#"):
            # Separate values
                cardId, name = [v.strip().lstrip("0") for v in line.split(",")]
                valid_names.append(name)
            if len(valid_names) > 2: break    # DEVELOPMENT

    valid_names.sort()

    # no args of specific names to check, so return list of all valid names
    if len(names) is 0: return valid_names

    # if one name in args is invalid, return false
    for n in names:
        if valid_names.count(n) is 0: return False

    # if we've made it this far, there *were* args and they all are valid names
    return True

# def synthesize_fortunes( ):
    '''
    AWS Polly requests take 30s on the pi, so we generate & cache a bunch of new
    ones every day quick UX
    '''


# def synthesize_motd( ):
    '''
    If there is a message of the day (motd) today, synthesize & cache it
    '''


def greeting_permutations (name="Unknown"):
    '''
    constructs iterable list of entry & exit greeting strings for a given user
    name or genericly-addressed strings if no name given.
    '''
    # probably should check to make sure name exists

def update_greetings(names=['Unknown']):
    '''
    permute & synthesize entry & exit greetings for new users; delete files
    for removed users.
    '''
    # https://docs.python.org/2/library/os.html?highlight=makedirs#os.makedirs
    for name in names:

        # create tty/greetings/<name>/[entry|exit] dirs
        for d in ["entry", "exit"]:
            assure_path_exists(
                os.path.join(tty_dir, 'greetings', name, d, '')
            )




# os.path.walk(path, visit, arg)
#	Calls the function visit with arguments (arg, dirname, names) for each
#	directory in the directory tree rooted at path (including path itself, if
#	it is a directory).
def update_tts():
    update_greetings(find_names())




# rewrite; belongs in access_control.py
# def playThemesong( msg ):
#
#     # say hello/goodbye (TODO make blocking)
#     subprocess.Popen("flite '" + msg + "'", shell=True)
#     time.sleep(2)
#
#     # select <name>.mp3 or default.mp3 if doesn't exist
#     song = '/data/music/default.mp3'
#
#     # if not already playing same song,
#     # play themesong
#     subprocess.Popen("mpg123 '" + song + "'", shell=True)
#
#         # something like
#         #   def play():
#         #       subprocess.Popen("flite 'echo Hello World'", shell=True, stdout=subprocess.PIPE)
#         #       subprocess.Popen("mpg123 /data/music/The_Final_Countdown_kazoo.mp3", shell=True, stdout=subprocess.PIPE)
#         #
#         # see executor
#         #   https://executor.readthedocs.io/en/latest/#api-documentation
#         # Popen deets
#         #   https://jimmyg.org/blog/2009/working-with-python-subprocess.html
#
#     # say inspirational message
