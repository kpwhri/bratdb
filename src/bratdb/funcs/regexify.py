import re

from loguru import logger

from bratdb.funcs.utils import get_output_path
from bratdb.nlp.stemmer import Stemmer


def regexify_keywords_to_file(extract, outpath=None, encoding='utf8',
                              extra_slop=1, **kwargs):
    _outpath = get_output_path(extract, outpath, exts=('regexify',))
    outpath = f'{_outpath}.tsv'
    code_pat = re.compile(r'\d+\.\d+')
    num_pat = re.compile(r'\d+')
    slop_pat = re.compile(r'\[W(?P<slop>\d+)<\|(?P<punct>.*?)\|>\]')
    regexes = []
    with open(extract, encoding=encoding) as fh:
        for line in fh:
            concept, keywords, term = line.strip().split('\t')
            words = []
            prev_word = False
            for word in term.split(' '):
                if code_pat.match(word):
                    regexes.append((concept, keywords, fr'\b{word}\b'))
                elif num_pat.match(word):
                    if prev_word:
                        words.append(r'\W*')
                    words.append(r'\d+')
                    prev_word = True
                elif slop_pat.match(word):
                    m = slop_pat.match(word)
                    cnt = int(m.group('slop')) + extra_slop
                    if '.' in m.group('punct') or ';' in m.group('punct'):
                        words.append(rf'\W*(\w+\W*){{0,{cnt}}}')
                    else:
                        words.append(rf'[^\w\.;]*(\w+[^\w\.;]*){{0,{cnt}}}')
                    prev_word = False
                else:  # is word
                    if prev_word:
                        words.append(r'\W*')
                    words.append(Stemmer.transform(word))
                    prev_word = True
            regexes.append((concept, keywords, ''.join(words)))

    with open(outpath, 'w', encoding=encoding) as out:
        out.write('\n'.join('\t'.join(line) for line in regexes))
