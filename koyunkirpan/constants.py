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

try:
  NO_REPLY = bool(strtobool(os.environ.get('NO_REPLY', default='True')))
  PYTHONENV = os.environ.get('PYTHONENV', default='development')

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

  path = Path('logs')
  path.mkdir(parents=True, exist_ok=True)
  BASE_LOG_DIR = os.environ.get('BASE_LOG_DIR', path.resolve().as_posix())

  logger.exception('Error occured while parse enviroment variables\n')
