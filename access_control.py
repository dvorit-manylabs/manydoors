#!/usr/bin/python
# Copyright 2015 Manylabs - MIT License
# Author: Elliott Dicus
#
# Copyright 2016 Manylabs - MIT License
# Author: Mac Cowell
# - port to docker/resin.io; add TTS + themesong system
#
# Script to respond to authorization requests from an Arduino powered RFID
# reader

import os
import serial
import time
import urllib
import urllib2
import ConfigParser
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

# may need to apt-get install pyserial
    # problems?
    # see https://forums.resin.io/t/problems-connecting-to-usb-serialport-from-container/24/2
#SERIAL_PORT = "/dev/ttyACM0"

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

idFile = "/app/ids.csv"
accessLog = "/data/accessLog.csv"

def watchForReport( port ):
    reportString = ''

    logger.info("Ready")

    # Start read loop
    while True:

        data = port.read()

        # Look for opening ('\x02') and closing bytes ('\x03'), otherwise store
        # the byte as long as it's not empty
        if data == '\x02':

            # Reset
            reportString = ''
        elif data == '\x03':
            logger.info("Checking ID -"), # Comma because we don't want a newline

            direction, cardId = reportString.split(":")

            logger.info("ID: %s" % cardId)

            # Reset
            reportString = ''

            processId( port, cardId, direction )

        elif data is not '':
            reportString += data

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

def letSlackKnow( text ):
    # Let slack know
    logger.info('slack posting in progress...')
    config = ConfigParser.ConfigParser()
    config.read('/data/access_control.ini') # TODO resin.io env variable instead?
    if 'slack.com' in config.sections():
        slackParams = {
            'token' : config.get('slack.com','Token'),
            'channel' : '#door',
            'text' : text,
            'as_user' : 'true'
        }
        try:
            urllib2.urlopen('https://slack.com/api/chat.postMessage?' + urllib.urlencode(slackParams), timeout=5)
        except urllib2.URLError, e:
            logger.error("error sending to slack")
        except socket.timeout, e:
            logger.error("timeout sending to slack")

        logger.info('slack posting done.')
    else:
        logger.info('please configure slack token in access_control.ini file')

def processId( port, cardId, direction ):
    name =  findNameForId( cardId )
    if name:

        # Record success
        recordAccess( cardId, direction, name, "Success: open strike" )

        # Respond to arduino
        port.write('\x02allowed\x03')

        # TODO reenable
        # letSlackKnow(direction + ' ' + name)
        logger.info('DEBUG skipping letSlackKnow(direction + \' \' + name)')
        playThemesong(direction + '. Hello, ' + name)

    else:

        # Record failure
        recordAccess( cardId, direction, detail="Failure: ID does not have access" )

        # Respond to arduino
        port.write('\x02denied\x03')

        if cardId.strip() != "0":
        	letSlackKnow( 'unsuccessful ' + direction + ' of unknown fob with id ' + cardId )


def findNameForId( decodedId ):
    with open( idFile, 'r', os.O_NONBLOCK ) as f:
        for line in f:

            # Ignore blank and commented lines
            if line and not line.startswith( "#" ):

                # Separate values
                cardId, name = [v.strip().lstrip("0") for v in line.split( "," )]
                # Make sure to compare strings
                if cardId == str(decodedId):
                    return name
    return None

def recordAccess(cardId="", direction="", name="", detail=""):
    with open( accessLog, 'a', os.O_NONBLOCK ) as f:

        # TODO: Record Survey responses

        # Lines are in the following format:
        # Timestamp, CardId, Direction, Name, Detail
        line = "%s, %s, %s, %s, %s\n" % ( str(datetime.now()), cardId, direction, name, detail )

        logger.info(line)

        f.write( line )
        f.flush()


def sigterm_handler(_signo, _stack_frame):
    "When sysvinit sends the TERM signal, cleanup before exiting."
    logger.info("[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] received signal {}, exiting...".format(_signo))

    sys.exit(0)

if __name__ == "__main__":

    # Open Serial Port
    # https://pyserial.readthedocs.io/en/latest/shortintro.html#opening-serial-ports
    portOpen = False
    while not portOpen:
        try:
            port = serial.Serial( SERIAL_PORT, baudrate=9600, timeout=0 )
            portOpen = True
        except serial.SerialException as e:
            logger.info("Could not open serial port. Trying again in 5 seconds.")
            portOpen = False
            time.sleep(5)

    # Start read loop
    try:
        watchForReport( port )
    except KeyboardInterrupt as e:
        pass
    except serial.SerialException as e:
        logging.info("Serial port disconnected. Quitting.")
