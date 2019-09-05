from collections import defaultdict, Counter

from loguru import logger

from bratdb.funcs.utils import get_output_path, load_brat_dump
from bratdb.term import Term


def get_keywords(bratdb, ignore_tags=None, keep_tags=None,
                 ignore_stopwords=False, **kwargs):
    ignore_tags = set(ignore_tags) if ignore_tags else {}
    keep_tags = set(keep_tags) if keep_tags else {}

    brat = load_brat_dump(bratdb)
    # collect all keywords
    ann_dict = defaultdict(int)  # concept, term -> frequency
    # look for overlapping keywords
    keyword_dict = defaultdict(list)  # keywords -> concept
    for annots in brat.annots.values():
        for annot_set in annots:
            for annot in annot_set.values():
                term = Term(annot.text, ignore_stopwords=ignore_stopwords)
                for label in annot.labels:
                    if keep_tags and label not in keep_tags:
                        continue
                    if label in ignore_tags:
                        continue
                    keyword_dict[term.keywordstr].append(label)
                    ann_dict[(label, term)] += 1
    return ann_dict, dict(filter(lambda x: len(x[1]) > 1, keyword_dict.items()))


def extract_keywords_to_file(bratdb, *, outpath=None,
                             sep='\t',
                             **kwargs):
    _outpath = get_output_path(bratdb, outpath, exts=('extract',))
    outpath = f'{outpath}.tsv'
    info_path = f'{outpath}.info'
    dupe_path = f'{outpath}.dupes'
    data, dupe_dict = get_keywords(bratdb, **kwargs)
    with open(outpath, 'w') as out:
        out.write('concept\tkeyword\tfreq\n')
        for (concept, keyword), freq in data.items():
            out.write(f'{concept}{sep}{keyword}{sep}{freq}\n')

    with open(dupe_path, 'w') as out:
        out.write('keyword\tconcepts\n')
        for keyword, concepts in dupe_dict.items():
            concepts = (f'{k} ({v})' for k, v in Counter(concepts).most_common())
            out.write(f'{keyword}\t{", ".join(concepts)}\n')
