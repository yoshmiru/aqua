import logging
from logging.handlers import RotatingFileHandler

def myLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    #handler = logging.StreamHandler()
    #handler = logging.FileHandler('aqua.log')
    handler = RotatingFileHandler('aqua.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = myLogger()
logger.debug('asdfasdfasdf')
