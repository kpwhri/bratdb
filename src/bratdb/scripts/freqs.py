from bratdb.funcs.frequency import build_frequency_file


def main():
    import argparse
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@!')
    parser.add_argument('bratdb',
                        help='Path to brat data dump (result of build script)')
    parser.add_argument('--outpath', default=None,
                        help='Output file containing frequencies')
    parser.add_argument('--title', default='Term Frequencies',
                        help='Title of output file')
    parser.add_argument('--not-once-per-document', default=True, action='store_false',
                        dest='once_per_document',
                        help='How to handle multiple versions of same document.')
    parser.add_argument('--max-length', dest='max_length', default=80, type=int,
                        help='Max length of text to include in output file')
    parser.add_argument('--dont-normalize', dest='normalize', default=True, action='store_false',
                        help='Include flag to not ignore case, and various other clean-up'
                             ' operations')
    args = parser.parse_args()
    build_frequency_file(**vars(args))


if __name__ == '__main__':
    main()
