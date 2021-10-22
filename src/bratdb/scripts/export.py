"""
Add two fields to the output of bratdb (`bdb-apply`) -- studyid and note_date.
    This will feed into an analytic dataset. The final dataset will
    contain the columns: 'doc_id', 'studyid', 'note_date', 'concept', 'term'.
    'studyid' and 'note_date' are not in the output of `bdb-apply`, so these will
    need to be added using the `--corpus-file` option. Alternatively, you can add
    'note_date' and 'studyid' to the `bdb-apply` output yourself.

# Prerequisites
    * Python 3.7+
    * pandas (`pip install pandas`): for reading datasets
    * loguru (`pip install loguru`): for logging

# Example runs

    * python --bdb-file C:\data\brat_dump.apply.tsv --corpus-file C:\data\corpus.csv
        - corpus.csv is assumed to have column names corresponding to 'document', 'studyid', and 'note_date'
        - otherwise, you'll need to run the following
    * python --bdb-file C:\data\brat_dump.apply.tsv --corpus-file C:\data\corpus.csv \
            --corpus-file-studyid-col study_id --corpus-file-date-col date --corpus-file-doc-col doc_id

# Input Arguments

## Required

    * --bdb-file PATH
        - input TSV file, the output of running `bdb-apply` on a dataset of notes
        - the file should have ".apply." embedded in it (unless a different output name was chosen)

## Optional
    * --output-dir PATH
        - default to same path as bdb-file
        - location to put output csv file
    * --corpus-file PATH
        - this process requires note_date and studyid fields
        - you can either add these directly to the bdb-file (ensure to keep it as a tsv) or supply a separate file
        - joining will be done based on `--corpus-file-doc-col` (defaults to 'document')
        - the names for the note_date and studyid fields should be specified under:
            - `--corpus-file-studyid-col`: defaults to `studyid`
            - `--corpus-file-date-col`: defaults to `note_date`

# Output
    * a CSV called 'nlp-by-patient_{datetime}.csv' in either directory supplied by --output-dir

"""
import csv
import datetime
import logging
import os
import pandas as pd
import pathlib
from loguru import logger


@logger.catch
def main(bdb_file: pathlib.Path, *, output_dir: pathlib.Path = None, corpus_file: pathlib.Path = None,
         corpus_file_doc_col='document', corpus_file_studyid_col='studyid',
         corpus_file_date_col='note_date'):
    if not output_dir:
        output_dir = bdb_file.parent
    output_dir.mkdir(exist_ok=True)
    logger.info(f'Output directory: {output_dir}')

    data = pd.read_csv(bdb_file, sep='\t', encoding='utf8')
    data.columns = data.columns.str.lower()
    data['document'] = data['document'].astype('int64')
    in_doc_ids = set(data['document'].unique())
    logger.info(f'Input file has {data.shape[0]} records with {len(in_doc_ids)} unique documents.')
    if corpus_file:
        corpus = pd.read_csv(corpus_file, encoding='utf8')
        corpus.columns = corpus.columns.str.lower()
        corpus = corpus[corpus[corpus_file_doc_col].notnull()]
        corpus[corpus_file_doc_col] = corpus[corpus_file_doc_col].astype('int64')
        corpus_doc_ids = set(corpus[corpus_file_doc_col].unique())
        logger.info(f'Corpus file has {len(corpus_doc_ids)} documents.')
        missing_in_docs = in_doc_ids - corpus_doc_ids
        if len(missing_in_docs) == 0:
            logging.info(f'Corpus file contains all documents present in bdb input file.')
        else:
            logging.warning(f'Corpus file is missing {len(missing_in_docs)} documents present in bdb input file.')
            logging.warning(f'Example corpus file documents missing:'
                            f' {", ".join(str(x) for x in list(missing_in_docs)[:4])}')
            logging.info(f'Continuing to process data.')
        df = pd.merge(data, corpus, left_on='document', right_on=corpus_file_doc_col)
    else:
        df = data

    with open(
            output_dir / f'nlp-by-patient_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            'w',
            newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['doc_id', 'studyid', 'note_date', 'concept', 'term'])
        for i, row in df.iterrows():
            writer.writerow([
                row[corpus_file_doc_col],
                row[corpus_file_studyid_col],
                row[corpus_file_date_col],
                row['concept'],
                row['term']
            ])


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('--bdb-file', dest='bdb_file', required=True, type=pathlib.Path,
                        help='Output file from `bdb-apply`.')
    parser.add_argument('--output-dir', dest='output_dir', default=None, type=pathlib.Path,
                        help='Directory to place output files. These will be automatically'
                             ' named with the timestamp, etc.')
    parser.add_argument('--corpus-file', dest='corpus_file', default=None, type=pathlib.Path,
                        help='File containing any missing columns from bdb-file'
                             ' (e.g., "studyid" and  "note_date").')
    parser.add_argument('--corpus-file-doc-col', dest='corpus_file_doc_col', default='document', type=str.lower,
                        help='Name of column to join to get extra data from.')
    parser.add_argument('--corpus-file-studyid-col', dest='corpus_file_studyid_col', default='studyid', type=str.lower,
                        help='Name of column in corpus file contianing studyid.')
    parser.add_argument('--corpus-file-date-col', dest='corpus_file_date_col', default='note_date', type=str.lower,
                        help='Name of column in corpus file containing date of the note.')
    main(**vars(parser.parse_args()))
