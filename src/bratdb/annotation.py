from collections import defaultdict


class Annotation(object):

    def __init__(self, key, text, spans, labels=()):
        self.key = key
        self.links = defaultdict(list)
        self.labels = defaultdict(list)
        self.attributes = {}
        for label in labels:
            self.labels[label] = []
        self.text = text
        self.spans = spans
        self.words = []

    @property
    def fullspan(self):
        return self.spans[0][0], self.spans[-1][1]

    def set(self, attribute, target):
        self.attributes[attribute] = target

    def __repr__(self):
        return f'{self.key}{self.labels.keys()}:"{self.text[:20]}"'