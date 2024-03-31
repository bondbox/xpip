# xpip

Python package. Build. Install.

## Language

- **[简体中文](docs/zh/README.md)**

## Features

- **Easily and quickly build and install Python package via [xpip-build](docs/xpip-build.md)**
- **Upload package to PyPI repository via [xpip-upload](docs/xpip-upload.md)**
- **Manage mirror via [xpip-mirror](docs/xpip-mirror.md)**

## Makefile

Create the following makefile for your project to easily and quickly build and upload Python package.

```Makefile
MAKEFLAGS += --always-make

all: build install


upgrade-xpip.build:
	pip3 install -i https://pypi.org/simple --upgrade xpip.build

upgrade-xpip.upload:
	pip3 install -i https://pypi.org/simple --upgrade xpip.upload

upgrade-xpip: upgrade-xpip.build upgrade-xpip.upload
	pip3 install -i https://pypi.org/simple --upgrade xpip.mirror


upload:
	xpip-upload --config-file .pypirc dist/*


build:
	xpip-build setup --clean --all


install:
	pip3 install --force-reinstall --no-deps dist/*.whl


uninstall:
	pip3 uninstall -y <package>
```
