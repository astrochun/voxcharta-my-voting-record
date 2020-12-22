# voxcharta-my-voting-record

- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Requirements](#requirements)
    - [Installation Instructions](#installation-instructions)
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

#### Python and setting up a environment

Using your preferred Python environment manager (`conda`, `venv`), you will
will create a separate environment. Below are `conda` instructions

```
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


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the [releases on this repository](https://github.com/astrochun/voxcharta-my-voting-record/releases).


## Authors

* Chun Ly, Ph.D. ([@astrochun](http://www.github.com/astrochun)) - [University of Arizona Libraries](https://github.com/ualibraries), [Office of Digital Innovation and Stewardship](https://github.com/UAL-ODIS)


## License

This project is licensed under the [GNU GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.en.html) - see the [LICENSE](LICENSE) file for details.
