#!/bin/bash

export WORKDIR=/home/koyunotlatan/service

# Set virtual enviroment directory as enviroment variable
export VIRTUAL_ENV=$WORKDIR/.venv

# Check $VIRTUAL_ENV enviroment variable exist
if [[ -n "$VIRTUAL_ENV" ]]; then
  # Create virtual enviroment if not exist
  if [[ ! -d "$VIRTUAL_ENV" ]]; then
    python3 -m venv $VIRTUAL_ENV
    chown -R koyunotlatan_ci:koyunotlatan $VIRTUAL_ENV
  fi

  # Install dependencies with virtual enviroment
  $VIRTUAL_ENV/bin/pip install -r $WORKDIR/requirements.txt
fi

systemctl daemon-reload
systemctl enable koyunotlatan.timer
systemctl start koyunotlatan.service
