from collections import defaultdict, Counter

from loguru import logger

from bratdb.funcs.utils import get_output_path, load_brat_dump
from bratdb.term import Term, TermSet


def get_keywords(bratdb, ignore_tags=None, keep_tags=None,
                 ignore_stopwords=False, **kwargs):
    ignore_tags = set(ignore_tags) if ignore_tags else {}
    keep_tags = set(keep_tags) if keep_tags else {}

    brat = load_brat_dump(bratdb)
    # collect all keywords
    ann_dict = TermSet()  # concept, term -> frequency
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
                    if term:  # are there any keywords here?
                        keyword_dict[term.keywordstr].append(label)
                        ann_dict.add(term, label)
        ann_dict.update()
    return ann_dict, dict(filter(lambda x: len(x[1]) > 1, keyword_dict.items()))


def extract_keywords_to_file(bratdb, *, outpath=None,
                             sep='\t', one_label_per_term=True,
                             encoding='utf8',
                             **kwargs):
    _outpath = get_output_path(bratdb, outpath, exts=('extract',))
    outpath = f'{_outpath}.tsv'
    freq_path = f'{_outpath}.freq.tsv'
    info_path = f'{_outpath}.info'
    dupe_path = f'{_outpath}.dupes'
    hapax_add_path = f'{_outpath}.add.hapax'
    hapax_omit_path = f'{_outpath}.omit.hapax'
    data, dupe_dict = get_keywords(bratdb, **kwargs)

    keyword_to_concept = {}  # store only most frequent label with each concept
    with open(dupe_path, 'w', encoding=encoding) as out:
        out.write('keyword\tconcepts\n')
        for keyword, concepts in dupe_dict.items():
            mc = Counter(concepts).most_common()
            concepts = (f'{k} ({v})' for k, v in mc)
            out.write(f'{keyword}\t{", ".join(concepts)}\n')
            if one_label_per_term:
                keyword_to_concept[keyword] = mc[0][0]

    terms = defaultdict(set)
    hapax_added = set()
    hapax_ignored = set()
    with open(freq_path, 'w', encoding=encoding) as out:
        out.write('concept\tterm\tfreq\n')
        for concept, keywordstr, freq in data.term_frequencies:
            # only keep majority term
            if not keyword_to_concept or keyword_to_concept.get(keywordstr, concept) == concept:
                out.write(f'{concept}{sep}{keywordstr}{sep}{freq}\n')

                if freq == 1:  # handle hapax legonoma
                    if data.get_freq(keywordstr) > 1:  # otherwise exists
                        terms[concept].add(keywordstr)
                    else:  # only retain known keywords
                        new_keyword = [kw for kw in data.get_term_keywords(keywordstr)
                                       if data.get_keyword_freq(kw) >= 2]
                        new_keyword_str = ' '.join(str(w) for w in new_keyword)
                        if data.get_freq(new_keyword_str) <= 1 and len(new_keyword) > 1:
                            term = data.get_term(keywordstr)
                            new_stopwords = {str(w) for w in data.get_term_keywords(keywordstr)
                                             if data.get_keyword_freq(w) < 2}
                            new_term = Term(term._orig_term, add_stopwords=new_stopwords)
                            terms[concept].add(new_keyword_str)
                            data.add(new_term, concept)
                            data.update()
                            hapax_added.add(new_keyword_str)
                        else:
                            hapax_ignored.add(keywordstr)
                else:
                    terms[concept].add(keywordstr)

    with open(hapax_add_path, 'w', encoding=encoding) as out:
        out.write('\n'.join(hapax_added))
    with open(hapax_omit_path, 'w', encoding=encoding) as out:
        out.write('\n'.join(hapax_ignored))
    with open(outpath, 'w', encoding=encoding) as out:
        for concept in terms:
            for keywordstr in terms[concept]:
                out.write(f'{concept}\t{keywordstr}\t{data.get_term(keywordstr).segmentstr}\n')
