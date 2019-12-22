# schroot-build-package
[![build](https://github.com/kiniou/schroot-build-package/workflows/build/badge.svg?branch=master)](https://github.com/kiniou/schroot-build-package/actions?query=workflow%3Abuild+branch%3Amaster)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This project is an opinionated alternative rewrite of `sbuild` with python.

## ✅ Installation

From PYPI (when it will be uploaded):
```shell
pip install schroot-build-package
```

From source:
```shell
pip install https+git://github.com/kiniou/schroot-build-package
```

## ⚙ Usage

Once installed, you'll be able to fire `sbp` in a command line which is a group of commands that'll help you to create build environment and build your packages:
```shell
Usage: sbp [OPTIONS] COMMAND [ARGS]...

  opinionated sbuild alternative

Options:
  -v, --verbose / --no-verbose  verbose logging
  -d, --debug / --no-debug      debug logging
  --help                        Show this message and exit.

Commands:
  build
  schroot  schroot related commands
```

## 👨‍💻 Hacking

If you want to hack this code and/or contribute with PR (❤), you can just fork
this repository and use editable pip mode installation within a virtualenv:
1. Create your python3 virtualenv:
```shell
$ python -m virtualenv -p $(which python3) .venv
```

2. Activate your fresh virtualenv:
```shell
$ . .venv/bin/activate
```

3. Install the project in editable mode:
```shell
(.venv) $ pip install -e .
```

Note that if you change some requirements, you'll need to update your virtualenv install as well:
```shell
pip install -U -e .
```

💡 If you need more dev tools (eg. ipython), extra packages can be installed with:
```shell
pip install -e ".[dev,testing]"
```
