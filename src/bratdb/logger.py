import os
import sys

from loguru import logger


def initialize_logging(logdir):
    logger.remove()
    logger.start(sys.stderr, level='INFO')
    logfile = 'bratdb_{time}.log'
    logpath = os.path.join(logdir, logfile)
    logger.add(logpath, level='DEBUG', rotation='0:01', compression='zip')
