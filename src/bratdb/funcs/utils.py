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
