import pathlib
import sys

from loguru import logger


def initialize_logging(logdir):
    if not logdir:
        logdir = '.'
    path = pathlib.Path(logdir)
    try:
        path.mkdir(exist_ok=True)
    except Exception as e:
        path = pathlib.Path('.')
    logger.remove()
    logger.start(sys.stderr, level='INFO')
    logger.add(path / 'bratdb_{time}.log', level='DEBUG')
