# voxcharta-my-voting-record

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/voxcharta-my-voting-record)
![PyPI](https://img.shields.io/pypi/v/voxcharta-my-voting-record?color=blue)
![License](https://img.shields.io/github/license/astrochun/voxcharta-my-voting-record?color=blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![PyPI - Downloads](https://img.shields.io/pypi/dm/voxcharta-my-voting-record?color=light%20green&label=pypi-download&style=flat-square)
![Hits](https://hitcounter.pythonanywhere.com/count/tag.svg?url=https%3A%2F%2Fgithub.com%2Fastrochun%2Fvoxcharta-my-voting-record)

- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Requirements](#requirements)
    - [Installation Instructions](#installation-instructions)
- [Vox Charta Data Export](#vox-charta-data-export)
- [Execution](#execution)
- [Versioning](#versioning)
- [Authors](#authors)
- [License](#license)

--------------

## Overview

This pure Python tool web scrapes data from [Vox Charta](https://voxcharta.org)'s
[My Voting Records page](https://voxcharta.org/tools/my-voting-record/).
It provides the data contents in two forms, a non-relational JSON file
and relational CSV file.

This software was driven by the need to archive such records since Vox Charta
will be sunsetted on December 31, 2020.


## Getting Started

These instructions will have the code running.


### Requirements

This software is tested with 3.10.2, the latest version available during recent development.
In principle it should work with >=3.7.  It requires `BeautifulSoup4` and `pandas`.


### Installation Instructions

#### Python and setting up an environment

Using your preferred Python environment manager (`conda`, `virtualenv`, `venv`),
I recommend create a separate environment to avoid any possible conflicts with
existing software that you used. Below are `conda` instructions

```:
$ (sudo) conda create -n voxcharta python=3.10.2
```

Installation is straightforward:

```
$ conda activate voxcharta
$ (sudo) pip install voxcharta-my-voting-record
```

Or from source:

```
$ conda activate voxcharta
$ git clone https://github.com/astrochun/voxcharta-my-voting-record.git
$ cd voxcharta-my-voting-record
$ (sudo) pip install .
```

For editable/development installation, execute `(sudo) pip install -e .`
This is preferred over the `python setup.py` method as certain dependencies (`numpy`) will fail to install during the build process.

## Vox Charta Data Export

Before using this software, you will want to export your Vox Charta My Voting Records
page. Here are the steps. These are based on Chrome, so differences may occur for other browsers:

1. [Login to Vox Charta](https://voxcharta.org/wp-login.php) before you can't!
2. Click on "Tools > My Voting Records"
3. After the page fully loads (this can take some time), click "File > Save Page As"
4. Change filename to "myvotingrecords"
5. For format, select "Webpage, Complete"

## Execution

The primary script to execute is [`vox_run`](bin/vox_run)

Execution requires only one argument, which is the full path
to the HTML file.

```
$ vox_run /full/path/to/myvotingrecords.htm
```

This is all possible using [`Typer`](https://typer.tiangolo.com/).
The script provides rich-formatted log messages to the terminal using [`Rich`](https://rich.readthedocs.io/).

All contents are stored in `/full/path/to` unless `outfile_prefix` is specified
with a different path. Thus, without specifying `outfile_prefix` the above execution
will generate:

 - JSON: `/full/path/to/myvotingrecords.json`
 - CSV: `/full/path/to/myvotingrecords.csv`

A log file is constructed: `/full/path/to/vox_run.YYYY-MM-DD.log`

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the [releases on this repository](https://github.com/astrochun/voxcharta-my-voting-record/releases).


## Authors

* Chun Ly, Ph.D. ([@astrochun](http://www.github.com/astrochun))


## License

This project is licensed under the [GNU GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.en.html) - see the [LICENSE](LICENSE) file for details.
