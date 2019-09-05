from bratdb.funcs.extract import extract_keywords_to_file
from bratdb.logger import initialize_logging


def main():
    import argparse

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('bratdb',
                        help='Path to brat data dump (result of build script)')
    parser.add_argument('--outpath', default=None,
                        help='Output file containing frequencies')
    parser.add_argument('--ignore-tags', dest='ignore_tags', default=None, nargs='+',
                        help='Ignore specified tags/labels;'
                             ' ignored if `keep-tags` is specified')
    parser.add_argument('--keep-tags', dest='keep_tags', default=None, nargs='+',
                        help='Keep only tags listed here; overrides `ignore-tags`')
    parser.add_argument('--ignore-stopwords', dest='ignore_stopwords', default=False, action='store_true',
                        help='Ignore stopwords')
    parser.add_argument('--allow-multiple-labels-per-term', dest='one_label_per_term',
                        default=True, action='store_false',
                        help='Allow all terms to be associated with more than one label/concept/term.')
    parser.add_argument('--logdir', default='.',
                        help='Directory to place log files.')
    args = parser.parse_args()
    initialize_logging(logdir=args.logdir)
    extract_keywords_to_file(**vars(args))


if __name__ == '__main__':
    main()
