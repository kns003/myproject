

import logging

log_file = '/tmp/test.log'
LOG_FORMAT = "%(asctime)s %(message)s"
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, 'a')
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
root_logger.addHandler(file_handler)
