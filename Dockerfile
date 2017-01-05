FROM resin/raspberrypi-python

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
	festival \
	festvox-don festvox-kallpc16k festvox-kdlpc16k festvox-rablpc16k \
	socat
	# Remove package lists to free up space
	# && rm -rf /var/lib/apt/lists/*

# here we set up the config for openSSH.
# https://github.com/resin-io-projects/resin-openssh/blob/master/Dockerfile.template
RUN mkdir /var/run/sshd \
    && echo 'root:resin' | chpasswd \
    && sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config \
		&& echo ". <(xargs -0 bash -c 'printf \"export %q\n\" \"\$@\"' -- < /proc/1/environ)" >> /root/.profile

# access_control.py requires pyserial
# 	use `RUN pip install -r /requirements.txt` for better container caching
#		if installing more python modules; use version pinning for reproducability:
#			echo 'pyserial==3.2.1' >> requirements.txt
RUN python -m pip install pyserial

# Defines our working directory in container
# WORKDIR /app

# copy current directory into /app
COPY . /app

# TODO notsure
# Enable systemd
ENV INITSYSTEM on

# does one-time setup tasks then execs access_control.py
CMD ["/bin/bash", "/app/doorbot_init.sh"]
