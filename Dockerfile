# Use an official python 3.11 image as a base
FROM python:3.11-slim-bullseye

WORKDIR /home/koyunkirpan/app

# Copy systemd service and timer units
COPY koyunkirpan.service koyunkirpan.timer /etc/systemd/system/

# Install systemd and dbus
RUN apt-get update
RUN apt-get install -y systemd systemd-sysv dbus dbus-user-session
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy python application
COPY koyunkirpan /home/koyunkirpan/app/koyunkirpan
COPY requirements.txt /home/koyunkirpan/app/

# Set virtual enviroment directory as enviroment variable
ENV VIRTUAL_ENV=/home/koyunkirpan/app/.venv
# Create virtual enviroment if not exist
RUN [ ! -d '$VIRTUAL_ENV' ] && python -m venv $VIRTUAL_ENV
# Add virtual enviroment binaries to the PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies with virtual enviroment
RUN pip install -r requirements.txt

ENTRYPOINT ["/sbin/init"]
