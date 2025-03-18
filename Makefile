MAKEFLAGS += --always-make

all: build install test


clean: build-clean test-clean


build-clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
build-xpip-mirror:
	python3 setup-mirror.py check sdist bdist_wheel --universal
build-xpip-upload:
	python3 setup-upload.py check sdist bdist_wheel --universal
build-xpip-build:
	python3 setup-build.py check sdist bdist_wheel --universal
build: build-clean build-xpip-mirror build-xpip-upload build-xpip-build


install-xpip-mirror:
	pip3 install --force-reinstall --no-deps dist/xpip-mirror-*.whl
install-xpip-upload:
	pip3 install --force-reinstall --no-deps dist/xpip-upload-*.whl
install-xpip-build:
	pip3 install --force-reinstall --no-deps dist/xpip-build-*.whl
install: install-xpip-mirror install-xpip-upload install-xpip-build

uninstall-xpip-mirror:
	pip3 uninstall -y xpip-mirror
uninstall-xpip-upload:
	pip3 uninstall -y xpip-upload
uninstall-xpip-build:
	pip3 uninstall -y xpip-build
uninstall: uninstall-xpip-mirror uninstall-xpip-upload uninstall-xpip-build

reinstall-xpip-mirror: uninstall-xpip-mirror install-xpip-mirror
reinstall-xpip-upload: uninstall-xpip-upload install-xpip-upload
reinstall-xpip-build: uninstall-xpip-build install-xpip-build
reinstall: reinstall-xpip-mirror reinstall-xpip-upload reinstall-xpip-build


upload-xpip-mirror:
	python3 -m twine check dist/xpip_mirror-*
	python3 -m twine upload --verbose --config-file .pypirc --repository xpip-mirror dist/xpip_mirror-*
upload-xpip-upload:
	python3 -m twine check dist/xpip_upload-*
	python3 -m twine upload --verbose --config-file .pypirc --repository xpip-upload dist/xpip_upload-*
upload-xpip-build:
	python3 -m twine check dist/xpip_build-*
	python3 -m twine upload --verbose --config-file .pypirc --repository xpip-build dist/xpip_build-*
upload: upload-xpip-mirror upload-xpip-upload upload-xpip-build


prepare-test:
	pip3 install --upgrade pylint flake8 pytest
pylint:
	pylint $$(git ls-files xpip_build/*.py)
	pylint $$(git ls-files xpip_mirror/*.py)
	pylint $$(git ls-files xpip_upload/*.py)
flake8:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
pytest:
	pytest xpip_build
	pytest xpip_mirror
	pytest xpip_upload
pytest-clean:
	rm -rf .pytest_cache
test: prepare-test pylint flake8 pytest
test-clean: pytest-clean
