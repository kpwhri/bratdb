class Stemmer:
    """
    Stemmer which provides regular expression variations
    """

    @staticmethod
    def replace(word, suffix, repl):
        res = word.rfind(suffix)
        base = word[:res]
        if len(base) < 4:
            return word + '(s|ing|ed)?'
        if base[-1] == base[-2]:
            base += '?'  # last letter was doubled
        return base + repl

    @staticmethod
    def transform(word):
        if word.endswith('sses'):
            word = Stemmer.replace(word, 'sses', 'ss(es|ing|ed)?')
        elif word.endswith('ies'):
            word = Stemmer.replace(word, 'ies', '(y|ies|ying|ied)?')
        elif word.endswith('ss'):
            word = Stemmer.replace(word, 'ss', 'ss(es|ing|ed)?')
        elif word.endswith('ch'):
            word = Stemmer.replace(word, 'ch', 'ch(es|ing|ed)?')
        elif word.endswith('s'):
            word = Stemmer.replace(word, 's', r'(s|\w?ing|\w?ed)?')
        elif word.endswith('eed'):
            word = Stemmer.replace(word, 'eed', r'ee(s|ing|d)?')
        elif word.endswith('ied'):
            word = Stemmer.replace(word, 'ied', '(y|ys|ies|ying|i?ed)?')
        elif word.endswith('ed'):
            word = Stemmer.replace(word, 'ed', r'e?(s|ing|d)?')
        elif word.endswith('ying'):
            word = Stemmer.replace(word, 'y', '(y|ys|ies|ying|i?ed)?')
        elif word.endswith('ing'):
            word = Stemmer.replace(word, 'ing', r'e?(s|ing|d)?')
        elif word.endswith('y'):
            word = Stemmer.replace(word, 'y', '(y|ys|ies|ying|i?ed)?')
        elif word.endswith('al'):
            word = Stemmer.replace(word, 'al', '(al)?e?(s|ing|d)?')
        else:
            word += '(s|ing|ed)?'
        return word
