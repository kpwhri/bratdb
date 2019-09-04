import os
import pickle
from collections import defaultdict


class BratCollection:  # TODO: make into 3.7 dataclass

    def __init__(self, *,
                 annotations=None,
                 sentences=None):
        self.annotations = annotations  # dict {document: [{T1: Annotation, ...}]
        self.sentences = sentences

    @property
    def annots(self):
        return self.annotations

    @property
    def sents(self):
        return self.sentences

    @property
    def doc_count(self):
        return len(self.annotations)

    def __iter__(self):
        for name in self.annotations:
            yield name, self.annotations[name], self.sentences[name]


def load_brat_dump(path, *, version=0):
    if version == 0:
        with open(path, 'rb') as fh:
            d = pickle.load(fh)
            annots, sents = defaultdict(list), {}
            for name in d:
                for annot, sent in d[name]:
                    annots[name].append(annot)
                    sents[name] = sent
            return BratCollection(annotations=annots, sentences=sents)
    elif version == 1:
        with open(path, 'rb') as fh:
            return pickle.load(fh)
    else:
        raise ValueError(f'Unknown version: {version}')


def get_output_path(target_path, outpath=None, exts=('txt',)):
    if outpath:  # outpath already exists
        return outpath
    path, fn = os.path.split(target_path)
    fn_elements = (fn.split('.')[0],) + exts
    outpath = os.path.join(path, '.'.join(fn_elements))
    return outpath
