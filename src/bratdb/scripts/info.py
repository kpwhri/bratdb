from bratdb.funcs.info import get_bratdb_info


def main():
    import argparse

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('bratdb',
                        help='Path to brat data dump (result of build script)')
    parser.add_argument('--outpath', default=None,
                        help='Output file containing frequencies')
    args = parser.parse_args()
    get_bratdb_info(**vars(args))
