import datetime
import os
import re

from loguru import logger

from bratdb.funcs.utils import get_output_path


def get_documents(directory=None, connection_string=None, query=None,
                  encoding='utf8', **kwargs):
    if directory:
        for root, dirs, files in os.walk(directory):
            for file in files:
                name = file.split('.')[0]
                fp = os.path.join(root, file)
                with open(fp, encoding=encoding, errors='ignore') as fh:
                    text = clean_text(fh.read().lower())
                yield name, text


def clean_text(text):
    return text.replace('\n', ' ').replace('\t', ' ')


def compile_regexes(regex_file, encoding='utf8'):
    """
    Reads and compiles regular expressions
    :param encoding:
    :param regex_file: concept \t term \t regex
    :return:
    """
    res = []
    with open(regex_file, encoding=encoding) as fh:
        for line in fh:
            concept, term, regex = line.strip().split('\t')
            res.append((concept, term, re.compile(regex)))
    return res


def apply_regex_to_corpus(regex, outpath=None, encoding='utf8', **kwargs):
    _outpath = get_output_path(regex, outpath, exts=('apply',))
    dt = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    outpath = f'{_outpath}.{dt}.tsv'
    logger.info(f'Primary output file: {outpath}')
    regexes = compile_regexes(regex, encoding)
    logger.info(f'Compiled {len(regexes)} regexes.')
    rx_cnt = 0
    with open(outpath, 'w') as out:
        out.write('document\tconcept\tcaptured\n')
        for i, (name, doc) in enumerate(get_documents(**kwargs)):
            for concept, term, regex in regexes:
                for m in regex.finditer(doc):
                    rx_cnt += 1
                    out.write(f'{name}\t{concept}\t{term}\t{m.group()}\n')
        if i % 1000 == 0:
            logger.info(f'Completed {i + 1} documents ({rx_cnt} concepts identified)')