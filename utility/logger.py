from __future__ import absolute_import
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(logger_name, log_file, level=logging.DEBUG):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(module)s [%(process)d %(thread)d] | [%(filename)s:%(lineno)s - %(funcName)s() ] | \n%(message)s')
    fileHandler = logging.handlers.RotatingFileHandler(log_file, maxBytes=102400000, backupCount=5, encoding='utf8')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)