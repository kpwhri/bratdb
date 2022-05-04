import datetime
import os
import re

from loguru import logger

from bratdb.funcs.utils import get_output_path


def get_documents(directory=None, extension='.txt',
                  connection_string=None, query=None,
                  encoding='utf8', **kwargs):
    if directory:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if extension and not file.endswith(extension):
                    continue
                name = file.split('.')[0]
                fp = os.path.join(root, file)
                with open(fp, encoding=encoding, errors='ignore') as fh:
                    text = clean_text(fh.read().lower())
                yield name, text
    elif connection_string and query:
        import sqlalchemy as sqla
        if isinstance(query, (list, tuple)):
            query = ' '.join(query)
        eng = sqla.create_engine(connection_string)
        for row in eng.execute(query):
            name = ','.join(str(x) for x in row[:-1])
            text = row[-1]
            yield name, text
    else:
        raise ValueError('Must specify either `directory` or'
                         ' both `connection_string` and `query`')


def clean_text(text):
    return text.replace('\n', ' ').replace('\t', ' ')


def compile_regexes(regex_file, encoding='utf8'):
    """
    Reads and compiles regular expressions
    :param encoding:
    :param regex_file: concept \t term \t regex
    :return:
    """
    res = []
    with open(regex_file, encoding=encoding) as fh:
        for line in fh:
            concept, term, regex = line.strip().split('\t')
            res.append((concept, term, re.compile(regex, re.IGNORECASE)))
    return res


def check_time_expired(start_time, run_hours):
    if not run_hours:
        return False
    return start_time + datetime.timedelta(hours=run_hours) > datetime.datetime.now()


def apply_regexes_to_text(regexes, text, newline_replace=' ',
                          exclude_captured=False, include_context: int = 0):
    for concept, term, regex in regexes:
        for m in regex.finditer(text):
            capture = '' if exclude_captured else m.group()
            capture = capture.replace('\n', newline_replace)
            if include_context:
                precontext = text[max(0, m.start() - include_context):m.start()].strip().replace('\n', newline_replace)
                postcontext = text[m.end():m.end() + include_context].strip().replace('\n', newline_replace)
                yield concept, term, capture, precontext, postcontext
            else:
                yield concept, term, capture


def apply_regex_to_df(regex, df, *, encoding='utf8', newline_replace=' ',
                      exclude_captured=False, include_context: int = 0):
    """Apply regular expressions to a dataframe rather than text.

    :param regex: file containing regular expressions in bratdb format
    :param df:
    :param encoding:
    :param newline_replace:
    :param exclude_captured:
    :param include_context: specify the amount of contextual characters to include.

    :return: list of tuples that can be loaded into pandas dataframe with
        pd.DataFrame(
            apply_regex_to_df(regex_file, df),
            columns=['id', 'concept', 'term', 'capture']
        )
        or
        pd.DataFrame(
            apply_regex_to_df(regex_file, df, include_context=100),
            columns=['id', 'concept', 'term', 'capture', 'precontext', 'postcontext']
        )
    """
    regexes = compile_regexes(regex, encoding)
    res = []
    for r in df.itertuples():
        for concept, term, capture, *rest in apply_regexes_to_text(
                regexes, r.note_text,
                include_context=include_context,
                newline_replace=newline_replace,
                exclude_captured=exclude_captured,
        ):
            if include_context:
                res.append((r.Index, concept, term, capture, rest[0], rest[1]))
            else:
                res.append((r.Index, concept, term, capture))
    return res


def apply_regex_to_corpus(regex, outpath=None, encoding='utf8',
                          run_hours=None, exclude_captured=False,
                          log_incr=10000, newline_replace=' ',
                          **kwargs):
    """
    :param regex:
    :param outpath:
    :param encoding:
    :param run_hours:
    :param exclude_captured:
    :param log_incr: number of records to run before reporting how long this many
        documents took to run
    :param kwargs:
    :return:
    """
    _outpath = get_output_path(regex, outpath, exts=('apply',))
    start_time = datetime.datetime.now()
    dt = start_time.strftime('%Y%m%d_%H%M%S')
    outpath = f'{_outpath}.{dt}.tsv'
    logger.info(f'Primary output file: {outpath}')
    regexes = compile_regexes(regex, encoding)
    logger.info(f'Compiled {len(regexes)} regexes.')
    rx_cnt = 0
    logger.info('Loading files.')
    with open(outpath, 'w', encoding=encoding) as out:
        out.write('document\tconcept\tterm\tcaptured\n')
        for i, (name, doc) in enumerate(get_documents(**kwargs)):
            for concept, term, regex in regexes:
                for m in regex.finditer(doc):
                    rx_cnt += 1
                    capture = '' if exclude_captured else m.group()
                    capture = capture.replace('\n', newline_replace)
                    out.write(f'{name}\t{concept}\t{term}\t{capture}\n')
            if i % log_incr == 0:
                logger.info(f'Completed {i + 1} documents ({rx_cnt} concepts identified)')
                if check_time_expired(start_time, run_hours):
                    logger.warning(f'Time expired.')
    logger.info(f'Process completed: {i + 1} documents in {datetime.datetime.now() - start_time}')
