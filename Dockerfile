FROM resin/raspberrypi-python

#####################################################################
# OPTIONAL - DEV environment
#		modify base image dpkg to allow groff device files to install
#		https://github.com/resin-io-library/base-images/issues/221
RUN sed -i '/groff/d' /etc/dpkg/dpkg.cfg.d/01_nodoc \
		&& sed -i '/man/d' /etc/dpkg/dpkg.cfg.d/01_nodoc
#####################################################################

# Install Python and flite deps.
# https://learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi/updating-alsa-config
RUN apt-get update \
	&& apt-get install -y \
		openssh-server \
		python \
		alsa-utils \
		libasound2-dev \
		mpg123 \
		flite \
		unzip \
		socat \
		fortunes fortune-mod \
	&& ln -s /usr/games/fortune /usr/local/bin
	# Remove package lists to free up space
	# && rm -rf /var/lib/apt/lists/*

# here we set up the config for openSSH.
# depends on openssh-server (above)
# https://github.com/resin-io-projects/resin-openssh/blob/master/Dockerfile.template
RUN mkdir /var/run/sshd \
    && echo 'root:resin' | chpasswd \
    && sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config \
		&& echo ". <(xargs -0 bash -c 'printf \"export %q\n\" \"\$@\"' -- < /proc/1/environ)" >> /root/.profile \
		&& echo "cd /app" >> /root/.bashrc

# access_control.py requires pyserial for talking to arduino/RFID
# 	use `RUN pip install -r /requirements.txt` for better container caching
#		if installing more python modules; use version pinning for reproducability:
#			echo 'pyserial==3.2.1' >> requirements.txt
RUN python -m pip install pyserial boto3

#####################################################################
# OPTIONAL - DEV environment
RUN apt-get install groff man \
		&& python -m pip install awscli
#####################################################################

# copy current directory into /app
COPY . /app

# TODO notsure
# Enable systemd
ENV INITSYSTEM on

# does one-time setup tasks then execs access_control.py
CMD ["/bin/bash", "/app/doorbot_init.sh"]
