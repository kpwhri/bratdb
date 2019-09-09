import datetime

from loguru import logger

from bratdb.funcs.utils import get_output_path


def apply_regex_to_corpus(regex, outpath=None, **kwargs):
    _outpath = get_output_path(regex, outpath, exts=('apply',))
    dt = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    outpath = f'{outpath}.{dt}.tsv'
