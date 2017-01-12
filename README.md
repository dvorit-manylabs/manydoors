# Manydoors Doorbot

ManyLabs has a collaborative DoorBot!  No one owns it; we all manage it together, from this page.

Purpose: Record and share tap-in, tap-out actions of members (with a ISO 14443A keyfob/card) and document workspace usage.

## Getting Started
1. Get a keyfob or keycard (if you have one already, you can use it)
2. Add your rfid number and name/alias to https://github.com/manylabs/manydoors/blob/master/ids.csv (ask for help if this is hard for you)
3. Tap-in and Tap-out when entering and leaving ManyLabs by placing your keyfob on the inside/outside facing coils on the door.
4. See your enter/exit actions on the Slack Channel

## features

1. use rfid to record entry/exit at the manylabs door.
2. automatically updates ids from this github repo when new ones are available
3. keeps a local event log on the pi
4. posts a enter/exit events on the [#door channel of manylabs slack](https://manylabs.slack.com/archives/door/)

# Code setup/ service maintenance

* Login to pi using ```ssh pi@door.local``` (ask for location and access credentials on Slack)

## new setup
* clone github repo using ```git clone https://github.com/manylabs/manydoors.git access_control```
* create a file ```access_control.ini``` with content like:
```
[slack.com]
Token=yourtoken
```
* create symlink to start service ```sudo ln -s /home/pi/rfid/access_control/access_control.conf /etc/init/access_control.conf```
* restart service using ```sudo service access_control restart```
* edit crontab for synching github repo ```crontab -e```
* add ```* * * * * cd /home/pi/rfid/access_control && git pull --rebase >> /home/pi/rfid/cronlog 2>&1```

## existing setup
* go to access_control folder ```cd rfid/access_control```
*  do whenever you need to do, probably ```git pull --rebase``` to get latest changes, or make config changes
*  restart service using ```sudo service access_control restart```

## Raspberry Pi configuration
- currently doorbot uses [Adafruit Occidentalis](https://github.com/adafruit/Adafruit-Occidentalis) rpi setup helper;
  - to configure network, edit file `/boot/occidentalis.txt`
  - this file can be edited directly on the SD card from another computer if network access is totally lost
- problems? check `/var/log/syslog`
  ```
  pi@door ~ $ sudo ifdown wlan0
  pi@door ~ $ sudo ifup wlan0  && tail -f /var/log/syslog
    # or
  localbox $ ssh pi@door.local "tail -f /var/log/syslog" 
  ```

## setup TTY
- install requirements (do this once):
  - `sudo ./init_tty.sh`
- add daily jobs to crontab?
- or use git-hooks?
