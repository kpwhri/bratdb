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
                        help='Output file containing frequencies')
    parser.add_argument('--run-hours', default=None, type=int, dest='run_hours',
                        help='End program after specified hours of running.')
    parser.add_argument('--logdir', default='.',
                        help='Directory to place log files.')
    parser.add_argument('--query', default=None, nargs='+',
                        help='query to retrieve name, document pairs from database table')
    args = parser.parse_args()
    initialize_logging(logdir=args.logdir)
    apply_regex_to_corpus(**vars(args))


if __name__ == '__main__':
    main()
