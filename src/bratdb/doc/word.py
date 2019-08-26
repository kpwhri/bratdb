class Word:

    def __init__(self, word, start, end, idx, sent_idx):
        self.word = word
        self.start = start
        self.end = end
        self.word_idx = idx
        self.sent_idx = sent_idx
        self._annotations = []

    def add_annotation(self, ann):
        self._annotations.append(ann)