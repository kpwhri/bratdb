import re

from bratdb.doc.word import Word


class Sentence:
    WORD_PAT = re.compile(r'\w')

    def __init__(self, sentence, idx, char_idx):
        self.sentence = sentence
        self.idx = idx
        self.start = char_idx
        self.end = self.start + len(sentence)
        self.words = []
        self._unpack_words()

    def _unpack_words(self):
        for i, m in enumerate(self.WORD_PAT.finditer(self.sentence)):
            word = Word(word=m.group(), start=self.start + m.start(),
                        end=self.end + m.start(), idx=i, sent_idx=self.idx)
            self.words.append(word)

    def get_span(self, start, end):
        for word in self.words:
            if word.start <= start < word.end:
                yield word
            if word.start <= end < word.end:
                yield word
            if start <= word.start < end and start < word.end < end:
                yield word