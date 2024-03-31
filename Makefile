MAKEFLAGS += --always-make

all: build install


build-clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

build-xpip.mirror:
	python3 setup-mirror.py check sdist bdist_wheel --universal

build-xpip.upload:
	python3 setup-upload.py check sdist bdist_wheel --universal

build-xpip.build:
	python3 setup-build.py check sdist bdist_wheel --universal

build: build-clean build-xpip.mirror build-xpip.upload build-xpip.build


install-xpip.mirror:
	pip3 install --force-reinstall --no-deps dist/xpip.mirror-*.whl

install-xpip.upload:
	pip3 install --force-reinstall --no-deps dist/xpip.upload-*.whl

install-xpip.build:
	pip3 install --force-reinstall --no-deps dist/xpip.build-*.whl

install: install-xpip.mirror install-xpip.upload install-xpip.build


uninstall-xpip.mirror:
	pip3 uninstall -y xpip.mirror

uninstall-xpip.upload:
	pip3 uninstall -y xpip.upload

uninstall-xpip.build:
	pip3 uninstall -y xpip.build

uninstall: uninstall-xpip.mirror uninstall-xpip.upload uninstall-xpip.build


upload-xpip.mirror:
	python3 -m twine check dist/xpip.mirror-*
	python3 -m twine upload --verbose --config-file .pypirc --repository xpip.mirror dist/xpip.mirror-*

upload-xpip.upload:
	python3 -m twine check dist/xpip.upload-*
	python3 -m twine upload --verbose --config-file .pypirc --repository xpip.upload dist/xpip.upload-*

upload-xpip.build:
	python3 -m twine check dist/xpip.build-*
	python3 -m twine upload --verbose --config-file .pypirc --repository xpip.build dist/xpip.build-*

upload: upload-xpip.mirror upload-xpip.upload upload-xpip.build
