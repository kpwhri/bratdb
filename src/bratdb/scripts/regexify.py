import argparse

from bratdb.funcs.regexify import regexify_keywords_to_file
from bratdb.logger import initialize_logging


def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('extract',
                        help='Extracted tsv file of bdb-extract process')
    parser.add_argument('--outpath', default=None,
                        help='Output file containing frequencies')
    parser.add_argument('--logdir', default='.',
                        help='Directory to place log files.')
    args = parser.parse_args()
    initialize_logging(logdir=args.logdir)
    regexify_keywords_to_file(**vars(args))


if __name__ == '__main__':
    main()
