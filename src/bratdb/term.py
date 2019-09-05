import re
import string

from bratdb.nlp.stopwords import get_stopwords


class Segment:
    STOPWORDS = get_stopwords()

    def __init__(self, term, is_punct=False):
        self.term = term
        self.is_punct = is_punct
        self.is_slop = self.term in self.STOPWORDS

    @property
    def is_keyword(self):
        return self.term and not self.is_punct and not self.is_slop


class Term:
    WORD_PAT = re.compile(r"([a-z]+('[a-z])?"
                          r'|[\d]+(\.[\d]+)?)')
    PUNCT = set(string.punctuation)

    def __init__(self, term):
        self._orig_term = term.strip().lower()
        self._segments = []
        prev = None
        for m in self.WORD_PAT.finditer(self._orig_term):
            if prev:
                self._segments.append(Segment(self.get_punctuation(prev, m.start()),
                                              is_punct=True))
            self._segments.append(Segment(m.group()))
            prev = m.end()
        self._keywords = tuple(w.term for w in self._segments if w.is_keyword)

    def get_punctuation(self, start, end):
        return set(self._orig_term[start:end]) & self.PUNCT

    @property
    def keywords(self):
        return self._keywords

    @property
    def segments(self):
        segs = []
        punct = set()
        slop = 0
        for w in self._segments:
            if w.is_keyword:
                if slop or punct:
                    if len(segs) > 0:  # don't add slop happening earlier
                        segs.append(f'[W{slop}<|{"".join(punct)}|>]')
                    slop = 0
                    punct = set()
                segs.append(f'{w.term}')
                continue

            if w.is_punct:
                punct |= w.term
            elif w.is_slop:
                slop += 1
        return tuple(segs)

    def __len__(self):
        return len(self._segments)

    def __eq__(self, other):
        if not isinstance(other, Term):
            return False
        return self._keywords == other._keywords

    def __hash__(self):
        return hash(self._keywords)
