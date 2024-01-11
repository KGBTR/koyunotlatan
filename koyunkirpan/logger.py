import sys
import logging
from datetime import datetime
from koyunkirpan.constants import BASE_LOG_DIR
# import logging.config

# logging.config.fileConfig("logger.ini")
logger = logging.getLogger('koyunkirpan')

formatter = logging.Formatter(
  fmt="%(asctime)s, (%(name)s:%(levelname)s) [%(filename)s:%(lineno)d]: %(message)s",
  datefmt="%d-%b-%Y %H:%M:%S"
)

fmt_date: str = "%d-%b-%Y"
formatted_today: str = datetime.today().strftime(fmt_date)

# Create handlers
# Create console handler
c_handler = logging.StreamHandler(sys.stdout)
"""
Console handler
"""
c_handler.setLevel(logging.INFO)
c_handler.setFormatter(formatter)

# Create error file Handler with ERROR level
f_err_handler = logging.FileHandler(filename=f'{BASE_LOG_DIR}/error-{formatted_today}.log')
"""
File handler with ERROR level powered by time rotate 
"""
f_err_handler.suffix = f'-{fmt_date}'
f_err_handler.setLevel(logging.WARNING)
f_err_handler.setFormatter(formatter)

# Create runtime file handler with INFO level
f_runtime_handler = logging.FileHandler(filename=f'{BASE_LOG_DIR}/runtime-{formatted_today}.log')
"""
File handler for runtime with INFO level powered by time rotate 
"""
f_runtime_handler.suffix = f'-{fmt_date}'
f_runtime_handler.setLevel(logging.INFO)
f_runtime_handler.setFormatter(formatter)

# Create debug file handler with INFO level
f_debug_handler = logging.FileHandler(filename=f'{BASE_LOG_DIR}/debug-{formatted_today}.log')
"""
File handler for debugging with DEBUG level powered by time rotate 
"""
f_debug_handler.suffix = f'-{fmt_date}'
f_debug_handler.setLevel(logging.DEBUG)
f_debug_handler.setFormatter(formatter)

logger.addHandler(c_handler)
logger.addHandler(f_err_handler)
logger.addHandler(f_runtime_handler)
logger.addHandler(f_debug_handler)

logger.info(f'Logger started at "{BASE_LOG_DIR}" directory')