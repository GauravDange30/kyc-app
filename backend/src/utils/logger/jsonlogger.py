import logging
import colorlog

# Define a custom logging formatter with color
log_format = '%(log_color)s%(levelname)-8s%(reset)s %(message)s'

log_colors = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'white,bg_red',
}

# Create a logger
logger = logging.getLogger('my_logger')
handler = logging.StreamHandler()

# Set the formatter with log colors
formatter = colorlog.ColoredFormatter(log_format, log_colors=log_colors)
handler.setFormatter(formatter)

# Add handler to the logger
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Example logs
logger.debug('This is a debug message.')
logger.info('This is an info message.')
logger.warning('This is a warning message.')
logger.error('This is an error message.')
logger.critical('This is a critical message.')
