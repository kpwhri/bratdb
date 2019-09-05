import datetime
import os
from collections import defaultdict
import pickle
from loguru import logger

from bratdb.nlp.sspl import sentencebreaks_to_list
from bratdb.annotation import Annotation
from bratdb.doc.sentence import Sentence


class TextFinder:
    """
    Iteratively search for text files as requested from *.ann files
    """

    def __init__(self, txt_dir, ignore_missing=True):
        """

        :param txt_dir: directory of brat "*.txt" files
        :param ignore_missing: if False, throw error if .txt file not found
        """
        self.txt_dir = txt_dir
        self.index = {}
        self._target = None
        self.ignore_missing = ignore_missing
        self._search = self._find_file()

    def __getitem__(self, item):
        if item in self.index:
            return self.index[item]
        elif os.path.exists(os.path.join(self.txt_dir, item)):
            return os.path.join(self.txt_dir, item)
        else:
            self._target = item
            try:
                return next(self._search)
            except StopIteration:
                err_msg = f'Failed to locate text file for {item}'
                if self.ignore_missing:
                    logger.warning(err_msg)
                    return None
                else:
                    raise FileNotFoundError(err_msg)

    def _find_file(self):
        for root, dirs, files in os.walk(self.txt_dir):
            for file in files:
                name = os.path.splitext(file)[0]
                if name == self._target:
                    yield os.path.join(root, file)
                self.index[name] = os.path.join(root, file)


def build_brat_dump(ann_dir, txt_dir, outdir='data'):
    """
    Dump brat data into intermediary format
    :param ann_dir:
    :param txt_dir:
    :param outdir:
    :return:
    """
    os.makedirs(outdir, exist_ok=True)
    counter = defaultdict(int)
    data = read_brat_directory(ann_dir, txt_dir, counter=counter)
    logger.info(f'Identified *.ann files: {counter["annfiles"]}')
    logger.info(f' - missing *.txt files: {counter["missing_text"]}')
    logger.info(f' - no annotations (possibly never reviewed): {counter["no_annotations"]}')
    total_count = counter['annfiles'] - counter['missing_text'] - counter['no_annotations']
    logger.info(f'Total annotation files added to dump: {total_count}')
    dt = datetime.datetime.now().strftime('%Y%m%d')
    with open(os.path.join(outdir, f'brat_dump_{dt}.pkl'), 'wb') as fh:
        pickle.dump(data, fh)


def read_brat_directory(ann_dir, txt_dir=None, counter=None):
    """Read brat directory (or directories)

    The first layer in ann_dir will be treated as a separate abstractor.

    :param ann_dir: directory containing annotation files
    :param txt_dir: directory containing text files (if different)
    :return:
    """
    text_finder = TextFinder(txt_dir or ann_dir)
    data = defaultdict(list)
    # if there is a 1st level, it's abstractor names
    for root, dirs, files in os.walk(ann_dir):
        for file in files:
            name, ext = os.path.splitext(file)
            if ext != '.ann':
                continue
            counter['annfiles'] += 1
            txt_path = text_finder[name]
            if not txt_path:
                logger.error(f'Unable to locate text file for annotation "{name}"')
                counter['missing_text'] += 1
                continue
            annotations = create_annotations(os.path.join(root, file), txt_path)
            if not annotations:
                counter['no_annotations'] += 1
                continue
            data[name].append(annotations)
    return data


def create_annotations(annfile, txtfile):
    """
    Create annotations from brat annotation and text files
    :param annfile:
    :param txtfile:
    :return:
    """
    with open(txtfile, encoding='utf8') as fh:
        text = fh.read()
    sents = []
    char_idx = 0
    for sent_idx, sent in enumerate(sentencebreaks_to_list(text)):
        sents.append(Sentence(sent, sent_idx, char_idx))
        char_idx += len(sent)
    ann_dict = defaultdict(dict)
    prev_ann = None
    with open(annfile, encoding='utf8') as fh:
        for idx, line in enumerate(fh):
            if not line.strip():  # empty line
                continue
            lst = line.strip().split('\t')
            if len(lst) < 2:
                logger.warning(f'Found continuation line: "{lst[0]}"')
                ann_dict[prev_ann[0]][prev_ann[1]][-1] += ' ' + lst[0]
                continue
            key = lst[0]
            letter = key[0]
            rest = lst[1:]
            ann_dict[letter][key] = rest
            prev_ann = (letter, key)
    if not ann_dict:
        logger.debug(f'No annotations found for file: {annfile}')
        return None

    annotations = {}
    events = defaultdict(list)  # event_key -> (affected Ts)
    # unpack T
    for key, rest in ann_dict['T'].items():
        label, *spans = rest[0].split()
        spans = get_spans(' '.join(spans))
        annotations[key] = Annotation(key,
                                      text='\t'.join(rest[1:]),
                                      spans=spans,
                                      labels=[label])
    # unpack 'E' for attributes only
    for key, rest in ann_dict['E'].items():
        for arg in rest[0].split():
            label, target_key = arg.split(':')
            events[key].append(target_key)
            # TODO: handle events
            if target_key[0] == 'E':
                continue
            annotations[target_key].set(label, 1)

    # unpack 'A' (attributes)
    for key, rest in ann_dict['A'].items():
        try:
            label, target_key = rest[0].split()
            val = 1
        except ValueError:
            label, target_key, val = rest[0].split()
        # TODO: handle events
        if target_key[0] == 'E':
            continue
        annotations[target_key].set(label, val)

    # add annotations to sentences
    for ann in annotations.values():
        for span in ann.spans:
            start, end = span
            for sent in sents:
                for word in sent.get_span(start, end):
                    ann.words.append(word)
                    word.add_annotation(ann)
    return annotations, sents


def get_spans(s):
    return [(int(ss.split()[0]),
             int(ss.split()[1]))
            for ss in s.split(';')]
