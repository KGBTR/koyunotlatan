# Use an official python 3.11 image as a base
FROM python:3.11-slim-bullseye

# Set user and group
ARG user=koyunotlatan
ARG uid=1000
RUN useradd -u ${uid} -U -s /bin/bash -m ${user}

# Install systemd and dbus
RUN apt-get update
RUN apt-get install -y systemd systemd-sysv dbus dbus-user-session policykit-1
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy polkit policy
COPY --chown=koyunotlatan:koyunotlatan koyunotlatan.pkla /etc/polkit-1/localauthority/50-local.d/

# Copy systemd service and timer units
COPY --chown=koyunotlatan:koyunotlatan koyunotlatan.service koyunotlatan.timer /etc/systemd/system/
# COPY --chown=koyunotlatan koyunotlatan.service koyunotlatan.timer /home/koyunotlatan/.config/systemd/user/

WORKDIR /home/${user}/service

# Set virtual enviroment directory as enviroment variable
ENV VIRTUAL_ENV=/home/${user}/service/.venv
# Create virtual enviroment if not exist
RUN [ ! -d '$VIRTUAL_ENV' ] && \
    python -m venv $VIRTUAL_ENV && \
    chown -R koyunotlatan:koyunotlatan $VIRTUAL_ENV
# Add virtual enviroment binaries to the PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy python application
COPY --chown=koyunotlatan:koyunotlatan koyunotlatan /home/${user}/service/koyunotlatan
COPY --chown=koyunotlatan:koyunotlatan requirements.txt /home/${user}/service/
COPY --chown=koyunotlatan:koyunotlatan praw.ini /home/${user}/.config/

# Install dependencies with virtual enviroment
RUN pip install -r /home/${user}/service/requirements.txt

ENTRYPOINT ["/sbin/init"]
