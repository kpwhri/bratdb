# bratdb

Prepare brat-formatted data for use in various NLP applications.  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 3.6+
    * loguru (`pip install loguru`) 
    * Other modules may be required to support, e.g., database access
        * sqlalchemy
        * pyodbc
        * etc.

### Installing

bratdb supports interacting with brat data via the command line.

Begin by cloning this repository and then installing the package

```
git clone git@github.com:kpwhri/bratdb.git
cd bratdb
python setup.py install
```

Get started by building a brat data dump (see below), and then use the various other functions to query/interact with the data.

### Functions

#### Build bratdump

This step is required to begin interacting with the brat data. It will create a dump (currently a pickle file) which the subsequent functions can then be applied.

```
bdb-build <annotation_dir> <text_dir> <output_dir>
```

* `annotation_dir`: directory containing brat's `*.ann` files, this can be the same as the `*.txt` files
* `text_dir`: directory containing brat's `*.txt` files, this can also have the `*.ann` files
* `output_dir`: directory to place brat dump
* `--logdir <logdir>`: optionally specify logging output directory

#### Get information on bratdb file

The brat dump is a bit inscrutable. You can use the `bdb-info` command to get some basic information about the pickle file.

```text
bdb-info <bratdb>
```
* `bratdb`: the file created from `bdb-build` (above)

#### Get term frequencies

Use the brat dump to generate term frequencies. To get a nice `*.rst` file you will need to install the [`pyscriven`](https://github.com/kpwhri/pyscriven) package (otherwise you'll get not-so-nice looking text file). You can then use [`pandoc`](https://pandoc.org/) to convert the `*.rst` file into a variety of formats.

```text
bdb-freq <bratdb>
``` 

* `bratdb`: the file created from `bdb-build` (above)
* `--outpath`: specify output file to write to
* `--title`: specify title of output file

#### Extract term keywords

One of the primary goals in getting annotated data is to use extract and deploy those keywords to markup other, unannotated data. In `bratdb` this requires 3 steps:

1. `bdb-extract`: extract keywords; these can then be manually manipulated for the build step
1. `bdb-extract-build`: convert the keywords into regular expressions
1. `bdb-apply`: 'tag' the keywords in a separate document dataset 

##### bdb-extract
Extract significant keywords from the `bratdb`. This process will produce several output files describing the work done.


```text
bdb-extract <bratdb>
``` 

* `bratdb`: the file created from `bdb-build` (above)
* `--outpath`: specify output file to write to
* `--keep-tags`: specify which tags should be output
* `--ignore-tags`: specify which tags to ignore
* `--logdir`: directory to place logging files 

Output files:
1. `*.extract.tsv`: primary output file which will be used as input to `bdb-extract-build`
2. `*.extract.freq.tsv`: show the frequency of each annotated `concept, term` pair
3. `*.extract.dupes`: often, the same term will be assigned multiple categories/concepts/labels; this document lists the variations
4. `*.extract.add.hapax`: lists the single-occuring terms which were still identified as useful; it may be worthwhile to review and ensure that no useless combinations were included
5. `*.extract.omit.hapax`: lists the single-occurring terms which were omitted from the termlist; it may be worthwhile to review and ensure that no potentially useful terms were left out


##### bdb-extract-build (regexify)
Convert the extracted terms into regular expressions.

```text
bdb-extract-build <extract>
``` 

* `extract`: the file created from `bdb-extract` (above), name like `*.extract.tsv`
* `--outpath`: specify output file to write to
* `--logdir`: directory to place logging files 

##### bdb-apply
Use the extracted terms (built into regular expressions) to identify concepts in text.

```text
bdb-apply <regex>
``` 

* `regex`: the file created from `bdb-extract-build` (above); name like `*.regexify.tsv` 
* `--outpath`: specify output file to write to
* `--run-hours`: specify maximum amount of time you want the application to run
* `--logdir`: directory to place logging files 
* `--exclude-captured`: exclude captured text (ergo, include only metadata and no PII in output file)

Reading from the file system:
* `--directory`: specify topmost directory of files
* `--extension`: only process files with this extension (default: `.txt`)

Reading from database:
* required: `sqlalchemy` and any dependencies for the connection (e.g., `pyodbc`)
* `--connection-string`: sqlalchemy-like connection string
    * this is the argument passed into `sqlalchemy.create_engine` (see [sqlalchemy docs](https://docs.sqlalchemy.org/en/13/core/engines.html))
    * e.g., `--connection-string "mssql+pyodbc://@SERVER/database?driver=SQL Server"`
* `--query`: query to run, which should give (name, document_text) tuples

##### bdb-clean
Expressions which generate the same stemmed/regex form. For example "depressed" and "depresses" will both generate the same regex form. This can also be useful after a `merge`

```text
bdb-clean <regex_or_extract>
``` 

* `regex_or_extract`: the file created from `bdb-extract` or `bdb-extract-build` (above); name like `*.regexify.tsv` or `*.extract.tsv`  
* `--outpath`: specify output file to write to
* `--logdir`: directory to place logging files 

##### bdb-merge
Merge multiple `*.extract.tsv` files.

```text
bdb-merge <extract> <extract> ...
``` 

* `extract`: supply each `*.extract.tsv` file to merge as a separate argument   
* `--outpath`: specify output file to write to
* `--logdir`: directory to place logging files 


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/kpwhri/bratdb/tags). 


## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.


## Roadmap

* Term frequency functions
* Long annotation cleanup
* Validation tests
* General test coverage
