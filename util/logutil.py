import logging

__author__ = 'tangz'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def info(msg):
    logging.info(msg)