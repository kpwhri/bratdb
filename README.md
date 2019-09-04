# bratdb

Prepare brat-formatted data for use in various NLP applications.  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 3.6
    * loguru (`pip install loguru`) 

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

* annotation_dir: directory containing brat's `*.ann` files, this can be the same as the `*.txt` files
* text_dir: directory containing brat's `*.txt` files, this can also have the `*.ann` files
* output_dir: directory to place brat dump
* `--logdir <logdir>`: optionally specify logging output directory

#### Get term frequencies

Use the brat dump to generate term frequencies. To get a nice `*.rst` file you will need to install the [`pyscriven`](https://github.com/kpwhri/pyscriven) package (otherwise you'll get not-so-nice looking text file). You can then use [`pandoc`](https://pandoc.org/) to convert the `*.rst` file into a variety of formats.

```text
bdb-freq <bratdb_file>
``` 

* bratdb_file: the file created from `bdb-build` (above)
* --outpath: specify output file to write to
* --title: specify title of output file

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/kpwhri/bratdb/tags). 


## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.


## Roadmap

* Term frequency functions
* Long annotation cleanup
* Validation tests
* General test coverage
