import os
import re
from collections import defaultdict

from loguru import logger

from bratdb.funcs.utils import get_output_path


def merge_extracts(*extracts, outpath=None, encoding='utf8', **kwargs):
    if not extracts:
        extracts = kwargs['extracts']
    _outpath = get_output_path(extracts[0], outpath, exts=('extract.combined',))
    outpath = f'{_outpath}.tsv'
    keyword_to_concept = {}
    concept_to_term = defaultdict(lambda: defaultdict(str))
    for i, extract in enumerate(extracts):
        name = os.path.basename(extract)
        with open(extract, encoding=encoding) as fh:
            for line in fh:
                concept, keywords, term = line.strip().split('\t')
                if keywords in keyword_to_concept:
                    if keyword_to_concept[keywords] != concept:
                        logger.warning(f'Ignoring disagreement: "{name}" (extract #{i + 1}) classifies'
                                       f' "{keywords}" in "{concept}", expected: "{keyword_to_concept[keywords]}"')
                else:
                    keyword_to_concept[keywords] = concept

                if keywords in concept_to_term[concept]:
                    orig_term = concept_to_term[concept][keywords]
                    concept_to_term[concept][keywords] = merge_terms(orig_term, term)
                else:
                    concept_to_term[concept][keywords] = term

    with open(outpath, 'w', encoding=encoding) as out:
        for concept in concept_to_term:
            for keywordstr, term in concept_to_term[concept].items():
                out.write(f'{concept}\t{keywordstr}\t{term}\n')


def merge_terms(term1, term2):
    if term1 == term2:
        return term1
    slop_pat = re.compile(r'\[W(?P<slop>\d+)<\|(?P<punct>.*?)\|>\]')
    words1 = iter(term1.split(' '))
    words2 = iter(term2.split(' '))
    words = []
    for w1, w2 in zip(words1, words2):
        if w1 == w2:
            words.append(w1)
        else:
            m1 = slop_pat.match(w1)
            m2 = slop_pat.match(w2)
            if m1 and m2:
                slop = max(int(m1.group('slop')), int(m2.group('slop')))
                punct = ''.join(set(m1.group('punct')) | set(m2.group('punct')))
                words.append(f'[W{slop}<|{punct}|>]')
            elif m1:
                words.append(w1)
                w1 = next(words1)
                words.append(w1)
                if w1 != w2:
                    raise ValueError(f'Mismatch after slop: {w1} != {w2} in merge of ({term1} == {term2})')
            elif m2:
                words.append(w2)
                w2 = next(words2)
                words.append(w2)
                if w1 != w2:
                    raise ValueError(f'Mismatch after slop: {w1} != {w2} in merge of ({term1} == {term2})')
            else:  # is word
                raise ValueError(f'Words do not match: {w1} != {w2} in merge of ({term1} == {term2})')
    return ' '.join(words)
