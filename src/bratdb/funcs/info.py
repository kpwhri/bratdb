"""
Describe and provide information about the files
    generated by the bratdb package.
"""
from bratdb.funcs.utils import get_output_path


def get_bratdb_info(bratdb, *, outpath=None):
    outpath = get_output_path(bratdb, outpath)