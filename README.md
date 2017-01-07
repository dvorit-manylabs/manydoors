# Manydoors Doorbot

ManyLabs has a collaborative DoorBot!  No one owns it; we all manage it together, from this page.

Purpose: Record and share tap-in, tap-out actions of members (with a ISO 14443A keyfob/card) and document workspace usage.

## Getting Started
1. Get a keyfob or keycard (if you have one already, you can use it)
2. Add your rfid number and name/alias to https://github.com/jhpoelen/manydoors/blob/master/ids.csv (ask for help if this is hard for you)
3. Tap-in and Tap-out when entering and leaving ManyLabs by placing your keyfob on the inside/outside facing coils on the door.
4. See your enter/exit actions on the Slack Channel

## features
1. use rfid to record entry/exit at the manylabs door.
2. automatically updates ids from this github repo when new ones are available
3. keeps a local event log on the pi
4. posts a enter/exit events on the [#door channel of manylabs slack](https://manylabs.slack.com/archives/door/)
5. speaks entry/exit message at door
6. *BONUS*: plays silly theme song on entry

## roadmap
* switch from slack web api to streaming bot api; run hubot
* hubot server on RPI
* hubot actions to add/remove tokens
* hubot actions to upload & select silly theme songs

## code setup/ service maintenance
* Login to pi using ```ssh pi@door.local``` (ask for location and access credentials on Slack)


## new setup

### setup slack bot and get token
* create a new slack bot: visit [Manylabs Slack - Custom Integrations](https://manylabs.slack.com/apps/build/custom-integration) and select "Bots"
  * name it `doorbot`
  * save the auth token (note: should begin with `xoxb-`)
  * provide silly user icon
* from your own account within slack:
  * go to the [door](https://manylabs.slack.com/messages/door/) channel (join if necessary)
  * invite our new bot in: `/join @doorbot`
* check that doorbot auth key works:
```
curl -d 'token=<YOUR-BOT-AUTH-KEY-HERE>' \
  -d 'channel=#door' \
  -d 'text=web API chat.postMessage test spaces doorbot-test' \
  -d 'as_user=true' \
  -d 'pretty=1' \
  https://slack.com/api/chat.postMessage
```

### setup raspberry pi
* ~~clone github repo using ```git clone https://github.com/jhpoelen/manydoors.git access_control```~~
* create a file ```/data/access_control.ini``` with content like:
```
[slack.com]
Token=yourtoken
```
~~* create symlink to start service ```sudo ln -s /home/pi/rfid/access_control/access_control.conf /etc/init/access_control.conf```
* restart service using ```sudo service access_control restart```
* edit crontab for synching github repo ```crontab -e```
* add ```* * * * * cd /home/pi/rfid/access_control && git pull --rebase```~~

## existing setup
~~* go to access_control folder ```cd /data/access_control```
*  do whenever you need to do, probably ```git pull --rebase``` to get latest changes, or make config changes
*  restart service using ```sudo service access_control restart```~~

## references
* Slack [web API reference](https://api.slack.com/web) (what's we're using)
* Slack `chat.postMessage` [api documentation](https://api.slack.com/methods/chat.postMessage)


## dev notes

playing sounds
- learn about rpi ALSA
  - http://blog.scphillips.com/posts/2013/01/sound-configuration-on-raspberry-pi-with-alsa/
- aplay is built in to rpi resin.io image
- mpg123 is popular and installs ok
- grab songs from dropbox
  - wget -O songs.zip https://www.dropbox.com/sh/m502yddp4qr8til/AAAkaJgjKicYjvd8aTA-jQbqa?dl=1; unzip songs.zip

- cloud tts w/ AWS Polly
  - python streaming server example
    - http://docs.aws.amazon.com/polly/latest/dg/example-Python-server-code.html

- local tts
  - https://github.com/MycroftAI/mimic
  - better flite / festvox voices
  - https://ubuntuforums.org/showthread.php?t=751169

- fortune, motd, qotd, joke...
  - `apt-get install fortunes fortune-mod`
  - `printf "%s" "$(/usr/games/fortune -n 140 wisdom)" | flite `

time zone:
  - try `tzselect` command
    - `TZ='America/Los_Angeles'; export TZ`
  - doesn't seem to be working...

ssh access:
- get ip from resin.io dashboard
- ssh root@<ip-address> (pass=resin)
- TODO change passwd
- SSH refuse to connect, mentioning MTM worry?
  - remove key from local machine
  - ssh-keygen -R <YOUR-DEVICE'S-IP>
  - https://github.com/resin-io-projects/resin-openssh
- env variables not showing up in ssh terminal session?
  -
  - https://docs.resin.io/runtime/runtime/#using-resin-ssh-from-the-cli


## setting up AWS Polly for text-to-speech
1. Set up your AWS account and a AWS IAM account for [Amazon AWS Polly](https://aws.amazon.com/polly/) text-to-speech. See [Setting Up](http://docs.aws.amazon.com/polly/latest/dg/setting-up.html) section of the Amazon Polly docs or steps 1-2 of the [AWS S3 tutorial](https://aws.amazon.com/getting-started/tutorials/backup-to-s3-cli/) tutorial.
  - I used `brew install awscli` to get the command-line tools
  - create an AWS IAM user named 'doorbot'. Check the box for `programmatic access`. Leave `AWS management console` unchecked.
  - and attach the `AmazonPollyReadOnlyAccess` policy
  - note the values for the Access Key and Secret Access Key for the next step
2. [Configure environment variables](https://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variable-configuration) for the access keys using the [resin.io dashboard](https://dashboard.resin.io/apps/)
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_DEFAULT_REGION`: `us-west-2`
    - note: currently (Jan 2017) Polly is only available in US East (N. Virginia), US East (Ohio), US West (Oregon), and EU (Ireland) - see faq: [Q. In which regions is the service available?](https://aws.amazon.com/polly/faqs/)
