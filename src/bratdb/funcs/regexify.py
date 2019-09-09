from loguru import logger

from bratdb.funcs.utils import get_output_path


def regexify_keywords_to_file(extract, outpath=None):
    _outpath = get_output_path(extract, outpath, exts=('regexify',))
