import re
import string
from collections import defaultdict

from bratdb.nlp.stopwords import get_stopwords


class Segment:
    STOPWORDS = get_stopwords()

    def __init__(self, term, is_punct=False, ignore_stopwords=False):
        self.term = term
        self.is_punct = is_punct
        self.is_slop = not ignore_stopwords and self.term in self.STOPWORDS

    @property
    def is_keyword(self):
        return self.term and not self.is_punct and not self.is_slop


class Slop:

    def __init__(self, words: int, punct: set):
        self.words = words
        self.punct = punct
        self.is_slop = True
        self.is_keyword = False

    def __str__(self):
        return f'[W{self.words}<|{"".join(self.punct)}|>]'


class Keyword:

    def __init__(self, term: str):
        self.term = term
        self.is_slop = False
        self.is_keyword = True

    def __str__(self):
        return f'{self.term}'


class Term:
    WORD_PAT = re.compile(r"([a-z]+('[a-z])?"
                          r'|[\d]+(\.[\d]+)?)')
    PUNCT = set(string.punctuation)

    def __init__(self, term, ignore_stopwords=False, segments=None):
        self._orig_term = term.strip().lower()
        if segments:
            self._segments = list(segments)
        else:
            segs = []
            prev = None
            for m in self.WORD_PAT.finditer(self._orig_term):
                if prev:
                    segs.append(Segment(self.get_punctuation(prev, m.start()),
                                        is_punct=True,
                                        ignore_stopwords=ignore_stopwords))
                segs.append(Segment(m.group(),
                                    ignore_stopwords=ignore_stopwords))
                prev = m.end()
            self._segments = self.clean_segments(segs)
        self._keywords = tuple(w.term for w in self._segments if w.is_keyword)

    def get_punctuation(self, start, end):
        return set(self._orig_term[start:end]) & self.PUNCT

    @property
    def keywords(self):
        return self._keywords

    @property
    def keywordstr(self):
        return ' '.join(self.keywords)

    @property
    def segments(self):
        return tuple(str(w) for w in self._segments)

    def clean_segments(self, segs):
        res = []
        punct = set()
        slop = 0
        for w in segs:
            if w.is_keyword:
                if slop or punct:
                    if len(segs) > 0:  # don't add slop happening earlier
                        res.append(Slop(slop, punct))
                    slop = 0
                    punct = set()
                res.append(Keyword(w.term))
                continue

            if w.is_punct:
                punct |= w.term
            elif w.is_slop:
                slop += 1
        return tuple(res)

    def __len__(self):
        return len(self._segments)

    def __eq__(self, other):
        if not isinstance(other, Term):
            return False
        return self._keywords == other._keywords

    def __hash__(self):
        return hash(self._keywords)

    def __str__(self):
        return ' '.join(self.segments)

    def merge(self, other):
        if not isinstance(other, Term):
            raise ValueError(f'Expected type `Term` not `{type(other)}`')
        assert self.keywordstr == other.keywordstr, 'Can only merge Terms with shared keywords'
        segments = []  # shared segments
        oi = 0
        si = 0
        while si < len(self._segments):
            sw = self._segments[si]
            ow = other._segments[oi]
            if sw.is_keyword and ow.is_keyword:
                segments.append(sw)
                si += 1
                oi += 1
            elif sw.is_keyword and ow.is_slop:
                segments.append(ow)
                oi += 1
            elif sw.is_slop and ow.is_keyword:
                segments.append(sw)
                si += 1
            elif sw.is_slop and ow.is_slop:
                segments.append(Slop(words=max(sw.words, ow.words),
                                     punct=sw.punct | ow.punct))
                si += 1
                oi += 1
            else:
                raise ValueError(f'Unknown segments: {type(sw)}, {type(ow)}')
        return Term(self._orig_term, segments=segments)


class TermSet:

    def __init__(self):
        self._terms = dict()
        self.__curr_terms = set()
        self._freqs = defaultdict(int)

    def add(self, term: Term, label: str):
        s = term.keywordstr
        if s not in self._terms:
            self._terms[s] = term
            return
        prev = self._terms[s]
        self._terms[s] = term.merge(prev)
        self.__curr_terms.add((label, s))

    def update(self):
        """
        don't let multiple annotations in same doc influence the counts
        """
        for label, keywordstr in self.__curr_terms:
            self._freqs[(label, keywordstr)] += 1
        self.__curr_terms = set()

    @property
    def term_frequencies(self):
        if self.__curr_terms:
            self.update()
        for (label, keywordstr), freq in self._freqs.items():
            yield label, keywordstr, freq
