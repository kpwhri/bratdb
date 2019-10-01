import re

from loguru import logger

from bratdb.funcs.utils import get_output_path


def remove_duplicates(extract_or_regexify, outpath=None, encoding='utf8', **kwargs):
    _outpath = get_output_path(extract_or_regexify, outpath, exts=('clean',))
    outpath = f'{_outpath}.tsv'
    with open(extract_or_regexify, encoding=encoding) as fh:
        text = fh.read()
    # # both files have same format
    # if 'regexify' in extract_or_regexify:
    #     extract_file = False
    # elif 'extract' in extract_or_regexify:
    #     extract_file = True
    # elif re.search(r'\[W\d+<', text):  # is extract file
    #     extract_file = True
    # elif re.search(r'\\w\+', text):  # is regexify file
    #     extract_file = False
    # else:
    #     raise ValueError('Unrecognized file type: expected extract or regexify')

    existing_terms = {}
    for line in text.split('\n'):
        concept, name, term = line.split('\t')
        if term in existing_terms:
            c, n, t = existing_terms[term]
            logger.warning(f'Found duplicate term "{term}"')
            if concept != c:
                logger.warning(f'Concept differs: {concept} ({name}) vs {c} ({n})')
            if len(name) < len(n):  # keep the shortest/simplest spelling
                existing_terms[term] = (concept, name, term)
        else:
            existing_terms[term] = (concept, name, term)

    with open(outpath, 'w', encoding=encoding) as out:
        for c, n, t in existing_terms.values():
            out.write(f'{c}\t{n}\t{t}\n')
