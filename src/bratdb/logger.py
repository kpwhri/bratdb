import os
import sys

from loguru import logger


def initialize_logging(logdir):
    logger.remove()
    logger.start(sys.stderr, level='WARNING')
    logfile = 'bratdb_{time}.log'
    logpath = os.path.join(logdir, logfile)
    logger.add(logpath, level='INFO', rotation='0:01', compression='zip')
