from bratdb.funcs.extract import extract_keywords_to_file
from bratdb.logger import initialize_logging


def main():
    import argparse

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('bratdb',
                        help='Path to brat data dump (result of build script)')
    parser.add_argument('--outpath', default=None,
                        help='Output file containing frequencies')
    # TODO: add tags to ignore
    parser.add_argument('--logdir', default='.',
                        help='Directory to place log files.')
    args = parser.parse_args()
    initialize_logging(logdir=args.logdir)
    extract_keywords_to_file(**vars(args))


if __name__ == '__main__':
    main()
