# Use an official python 3.11 image as a base
FROM python:3.11-slim-bullseye

# Set user and group
ARG user=koyunkirpan
ARG uid=1000
RUN useradd -u ${uid} -U -s /bin/bash -m ${user}

# Install systemd and dbus
RUN apt-get update
RUN apt-get install -y systemd systemd-sysv dbus dbus-user-session policykit-1
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy polkit policy
COPY --chown=koyunkirpan:koyunkirpan koyunkirpan.pkla /etc/polkit-1/localauthority/50-local.d/

# Copy systemd service and timer units
COPY --chown=koyunkirpan:koyunkirpan koyunkirpan.service koyunkirpan.timer /etc/systemd/system/
# COPY --chown=koyunkirpan koyunkirpan.service koyunkirpan.timer /home/koyunkirpan/.config/systemd/user/

WORKDIR /home/${user}/service

# Set virtual enviroment directory as enviroment variable
ENV VIRTUAL_ENV=/home/koyunkirpan/service/.venv
# Create virtual enviroment if not exist
RUN [ ! -d '$VIRTUAL_ENV' ] && \
    python -m venv $VIRTUAL_ENV && \
    chown -R koyunkirpan:koyunkirpan $VIRTUAL_ENV
# Add virtual enviroment binaries to the PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy python application
COPY --chown=koyunkirpan:koyunkirpan koyunkirpan /home/koyunkirpan/service/koyunkirpan
COPY --chown=koyunkirpan:koyunkirpan requirements.txt /home/koyunkirpan/service/
COPY --chown=koyunkirpan:koyunkirpan praw.ini /home/koyunkirpan/.config/

# Install dependencies with virtual enviroment
RUN pip install -r /home/koyunkirpan/service/requirements.txt

ENTRYPOINT ["/sbin/init"]
