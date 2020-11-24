# PyBytom

[![Build Status](https://travis-ci.org/meherett/pybytom.svg?branch=master)](https://travis-ci.org/meherett/pybytom)
[![PyPI Version](https://img.shields.io/pypi/v/pybytom.svg?color=blue)](https://pypi.org/project/pybytom)
[![PyPI Python Version](https://img.shields.io/pypi/pyversions/pybytom.svg)](https://pypi.org/project/pybytom)
[![Coverage Status](https://coveralls.io/repos/github/meherett/pybytom/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/meherett/pybytom?branch=master)

Python library with tools for Bytom mainchain and sidechain protocols. [Wiki Documentation](https://github.com/meherett/pybytom/wiki)

## Installation

```
$ pip install pybytom
```

If you want to run the latest version of the code, you can install from git:

```
$ pip install git+git://github.com/meherett/pybytom.git
```

For the versions available, see the [tags on this repository](https://github.com/meherett/pybytom/tags).

## Development

We welcome pull requests. To get started, just fork this repository, clone it locally, and run:

```
$ pip install -e .[tests] -r requirements.txt
```

## Testing

You can run the tests with:

```
$ pytest
```

Or use `tox` to run the complete suite against the full set of build targets, or pytest to run specific 
tests against a specific version of Python.

## License

Distributed under the [MIT](https://github.com/meherett/pybytom/blob/master/LICENSE) license. See ``LICENSE`` for more information.
