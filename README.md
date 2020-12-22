# voxcharta-my-voting-record

![GitHub top language](https://img.shields.io/github/languages/top/astrochun/voxcharta-my-voting-record)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/astrochun/voxcharta-my-voting-record)
![GitHub](https://img.shields.io/github/license/astrochun/voxcharta-my-voting-record?color=blue)

- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Requirements](#requirements)
    - [Installation Instructions](#installation-instructions)
- [VoxCharta Data Export](#voxcharta-data-export)
- [Execution](#execution)
- [Versioning](#versioning)
- [Authors](#authors)
- [License](#license)

--------------

## Overview

This pure Python tool web scrapes data from [VoxCharta](https://voxcharta.org)'s
[My Voting Records page](https://arizona.voxcharta.org/tools/my-voting-record/).
It provides the data contents in two forms, a non-relational JSON file
and relational CSV file.

This software was driven by the need to archive such records since VoxCharta
will be sunsetted on December 31, 2020.


## Getting Started

These instructions will have the code running.


### Requirements

This software is tested with Python 3.9.1, the latest version available when
developed. In principle it should work with >=3.7.
It requires `BeautifulSoup4` and `pandas`.


### Installation Instructions

#### Python and setting up an environment

Using your preferred Python environment manager (`conda`, `venv`), I recommend
create a separate environment to avoid any possible conflicts with
existing software that you used. Below are `conda` instructions

```:
$ (sudo) conda create -n voxcharta python=3.9.1
```

Installation is straightforward:
```
$ conda activate voxcharta
$ git clone https://github.com/astrochun/voxcharta-my-voting-record.git
$ cd voxcharta-my-voting-record
$ (sudo) python setup.py install
```

When this is "PyPi"-ed:
```
$ conda activate voxcharta
$ (sudo) pip install voxcharta-my-voting-record
```

## VoxCharta Data Export

Before using this software, you will want to export your VoxCharta My Voting Records
page. Here are the steps. These are based on Chrome, so differences may occur:

1. [Login to VoxCharta](https://voxcharta.org/wp-login.php) before you can't!
2. Click on "Tools > My Voting Records"
3. After the page fully loads (this can take some time), click "File > Save Page As"
4. Change filename to "myvotingrecords"
5. For format, select "Webpage, Complete"

## Execution

The primary script to execute is [`vox_run`](bin/vox_run)

Execution requires only one argument, which is the full path
to the HTML file. It can be provided with the `-f` or `--filename` 
command-line flags.

```
$ vox_run -f /full/path/to/myvotingrecords.htm
```

All contents are stored in `/full/path/to`. Unless `-j`/`--json_outfile` and
`-c`/`--csv_outfile` flags are provided, these are the output files are:

 - JSON: `/full/path/to/myvotingrecords.json`
 - CSV: `/full/path/to/myvotingrecords.csv`

A log file is constructed: `/full/path/too/vox_run.YYYY-MM-DD.log`

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the [releases on this repository](https://github.com/astrochun/voxcharta-my-voting-record/releases).


## Authors

* Chun Ly, Ph.D. ([@astrochun](http://www.github.com/astrochun)) - [University of Arizona Libraries](https://github.com/ualibraries), [Office of Digital Innovation and Stewardship](https://github.com/UAL-ODIS)


## License

This project is licensed under the [GNU GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.en.html) - see the [LICENSE](LICENSE) file for details.
