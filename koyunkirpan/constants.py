import os
from pathlib import Path
from distutils.util import strtobool
import logging
from typing import Literal

logger = logging.getLogger('koyunkirpan')

NO_REPLY: bool
PYTHONENV: Literal['development', 'production']
BASE_LOG_DIR: str
"""
Base log directory
"""

BOT_CLIENT_ID: str
BOT_CLIENT_SECRET: str
BOT_USERNAME: str
BOT_PASSWORD: str
BOT_ACTIVE_SUBREDDITS: str

try:
  NO_REPLY = bool(strtobool(os.environ.get('NO_REPLY', default='True')))
  PYTHONENV = os.environ.get('PYTHONENV', default='development')

  BOT_CLIENT_ID = os.environ.get('BOT_CLIENT_ID', default='')
  BOT_CLIENT_SECRET = os.environ.get('BOT_CLIENT_SECRET', default='')
  BOT_USERNAME = os.environ.get('BOT_USERNAME', default='')
  BOT_PASSWORD = os.environ.get('BOT_PASSWORD', default='')
  BOT_ACTIVE_SUBREDDITS = os.environ.get('BOT_ACTIVE_SUBREDDITS', default='KGBTR')

  if PYTHONENV == 'development':
    path = Path('logs')
    path.mkdir(parents=True, exist_ok=True)

    BASE_LOG_DIR = os.environ.get('BASE_LOG_DIR', path.resolve().as_posix())
  elif PYTHONENV == 'production':
    path = Path('/var/log/koyunkirpan')
    path.mkdir(parents=True, exist_ok=True)

    BASE_LOG_DIR = os.environ.get('BASE_LOG_DIR', path.resolve().as_posix())
except Exception:
  NO_REPLY = True
  PYTHONENV = 'development'

  BOT_CLIENT_ID = ''
  BOT_CLIENT_SECRET = ''
  BOT_USERNAME = ''
  BOT_PASSWORD = ''
  BOT_ACTIVE_SUBREDDITS = 'KGBTR'

  path = Path('logs')
  path.mkdir(parents=True, exist_ok=True)
  BASE_LOG_DIR = os.environ.get('BASE_LOG_DIR', path.resolve().as_posix())

  logger.exception('Error occured while parse enviroment variables\n')
