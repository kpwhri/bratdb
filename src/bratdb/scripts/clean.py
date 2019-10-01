import argparse

from bratdb.funcs.clean import remove_duplicates
from bratdb.logger import initialize_logging


def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('extract_or_regexify',
                        help='Extracted tsv file of bdb-extract process')
    parser.add_argument('--outpath', default=None,
                        help='Output file containing frequencies')
    parser.add_argument('--logdir', default='.',
                        help='Directory to place log files.')
    args = parser.parse_args()
    initialize_logging(logdir=args.logdir)
    remove_duplicates(**vars(args))


if __name__ == '__main__':
    main()
