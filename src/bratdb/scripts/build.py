from bratdb.reader import build_brat_dump
from bratdb.logger import initialize_logging


def main():
    import argparse

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@!')
    parser.add_argument('anndir',
                        help='Path to directory containing brat annotation files')
    parser.add_argument('txtdir', default=None,
                        help='Path to directory containing brat annotation files')
    parser.add_argument('outdir', default='bratdb',
                        help='Path to output directory where brat data will be stored.')
    parser.add_argument('--logdir', default='.',
                        help='Directory to place log files.')
    args = parser.parse_args()

    initialize_logging(logdir=args.logdir)
    build_brat_dump(args.anndir, args.txtdir, args.outdir)


if __name__ == '__main__':
    main()
