import itertools
import os
from collections import Counter, defaultdict

try:
    PYSCRIVEN = True
    from pyscriven import RestWriter, Table, tabulate_dict_counter
except ImportError:
    PYSCRIVEN = False

from bratdb.funcs.utils import load_brat_dump, get_output_path


def build_simple_freq_file(freqs, ofp):
    with open(ofp, 'w') as out:
        out.write('Term Frequncies\n\n')
        for label, cntr in freqs.items():
            out.write(f'{label}\n')
            out.write('=' * len(label) + '\n')
            for term, cnt in sorted(cntr.items(), key=lambda x: -x[1]):
                out.write(f'{term:.<90}.{cnt:.>10}\n')
            out.write('\n')


def build_frequency_file(bratdb, *, outpath=None, title='Term Frequency', **kwargs):
    outpath = get_output_path(bratdb, outpath,
                              exts=('freq', 'rst' if PYSCRIVEN else '.txt'))
    freqs = get_frequency(bratdb, **kwargs)
    if not PYSCRIVEN:
        return build_simple_freq_file(freqs, outpath)

    rst_list = [('heading', title)]
    for label, datum in tabulate_dict_counter(freqs,
                                              fillvalue='-',
                                              as_items=True):
        rst_list.append(('heading', label, {'level': 2}))
        rst_list.append(('table', Table(header=('Annotation', 'Term', 'Frequency'),
                                        data=datum)))
    with RestWriter(fp=outpath) as out:
        out.write_all(rst_list)


def get_frequency(bratdb, *, dbversion=0, once_per_document=True,
                  max_length=80, normalize=True):
    """

    :param normalize: cleanup various forms to some canonical
    :param max_length:
    :param bratdb: path to bratdb dump
    :param dbversion: version of dumped brat data to use
    :param once_per_document: if IRR record, only take one of the results
    :return:
    """
    data = load_brat_dump(bratdb, version=dbversion)
    counter = defaultdict(Counter)
    for docid, doc_annots in data.annots.items():
        if once_per_document:
            annots = max(doc_annots, key=len).items()  # if IRR reviewed, select most complete
        else:
            annots = itertools.chain(*(x.items() for x in doc_annots))
        for key, annot in annots:
            text = annot.text.strip()
            if normalize:
                text = text.lower()
            for label in annot.labels:
                counter[label][text[:max_length]] += 1
    return counter
