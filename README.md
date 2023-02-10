# brutal-bag

[![PyPI](https://img.shields.io/pypi/v/brutal-bag.svg)](https://pypi.org/project/brutal-bag/)
[![Changelog](https://img.shields.io/github/v/release/thavelick/brutal-bag?include_prereleases&label=changelog)](https://github.com/thavelick/brutal-bag/releases)
[![Tests](https://github.com/thavelick/brutal-bag/workflows/Test/badge.svg)](https://github.com/thavelick/brutal-bag/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/thavelick/brutal-bag/blob/master/LICENSE)

A js-optional frontend for Wallabag

## Installation

Install this tool using `pip`:

    pip install brutal-bag

## Usage

For help, run:

    brutal-bag --help

You can also use:

    python -m brutal_bag --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd brutal-bag
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
