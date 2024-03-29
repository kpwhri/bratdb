import argparse

from bratdb.funcs.apply import apply_regex_to_corpus
from bratdb.logger import initialize_logging


def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('regex',
                        help='Regex tsv file of bdb-extract-regex process;'
                             ' concept {tab} term {tab} regex')
    parser.add_argument('--directory', default=None,
                        help='Directory containing files to process')
    parser.add_argument('--extension', default='.txt',
                        help='Only process files with this extension')
    parser.add_argument('--connection-string', default=None, dest='connection_string',
                        help='sqlalchemy-flavored connection string')
    parser.add_argument('--outpath', default=None,
                        help='Output directory to place result.')
    parser.add_argument('--exclude-captured', default=False, action='store_true', dest='exclude_captured',
                        help='Only retain metadata; Exclude captured text as this may contain PII')
    parser.add_argument('--run-hours', default=None, type=int, dest='run_hours',
                        help='End program after specified hours of running.')
    parser.add_argument('--logdir', default=None,
                        help='Directory to place log files. If not specified, defaults to output directory.')
    parser.add_argument('--query', default=None, nargs='+',
                        help='query to retrieve name, document_text pairs from database table;'
                             ' additional items can be included, but text must be last')
    args = parser.parse_args()
    initialize_logging(logdir=args.logdir or args.outpath)
    apply_regex_to_corpus(**vars(args))


if __name__ == '__main__':
    main()
