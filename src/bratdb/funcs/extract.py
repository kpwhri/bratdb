from collections import defaultdict

from loguru import logger

from bratdb.funcs.utils import get_output_path, load_brat_dump
from bratdb.term import Term


def get_keywords(bratdb, ignore_tags=None, keep_tags=None,
                 ignore_stopwords=False, **kwargs):
    brat = load_brat_dump(bratdb)
    # collect all keywords
    ann_dict = defaultdict(int)  # concept, term -> frequency
    # look for overlapping keywords
    keyword_dict = defaultdict(set)  # keywords -> concept
    for annots in brat.annots.values():
        for annot_set in annots:
            for annot in annot_set.values():
                term = Term(annot.text)
                for label in annot.labels:
                    keyword_dict[term.keywordstr].add(label)
                    ann_dict[(label, term)] += 1
    return ann_dict, dict(filter(lambda x: len(x[1]) > 1, keyword_dict.items()))


def extract_keywords_to_file(bratdb, *, outpath=None,
                             sep='\t',
                             **kwargs):
    outpath = get_output_path(bratdb, outpath, exts=('extract', 'tsv'))
    info_path = f'{outpath}.info'
    data, dupe_dict = get_keywords(bratdb, **kwargs)
    with open(outpath, 'w') as out:
        out.write('concept\tkeyword\tfreq\n')
        for (concept, keyword), freq in data.items():
            out.write(f'{concept}{sep}{keyword}{sep}{freq}\n')

    with open(info_path, 'w') as out:
        out.write('keyword\tconcepts\n')
        for keyword, concepts in dupe_dict.items():
            out.write(f'{keyword}\t{", ".join(concepts)}\n')
