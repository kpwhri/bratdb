from bratdb.funcs.info import build_bratdb_info_file


def main():
    import argparse

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('bratdb',
                        help='Path to brat data dump (result of build script)')
    parser.add_argument('--outpath', default=None,
                        help='Output file containing frequencies')
    args = parser.parse_args()
    build_bratdb_info_file(**vars(args))


if __name__ == '__main__':
    main()
