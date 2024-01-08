from os import environ
from distutils.util import strtobool
import logging
from typing import TYPE_CHECKING

import koyunkirpan.logger

logger = logging.getLogger('koyunkirpan')

try:
  NO_REPLY: bool = bool(strtobool(environ.get('NO_REPLY', default='True')))
except Exception:
  NO_REPLY: bool = True
  logger.exception('\nError occured while parse to `NO_REPLY` enviroment variable\n')
