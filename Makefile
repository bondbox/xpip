MAKEFLAGS += --always-make

all: build install test


clean: build-clean test-clean


build-clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
build-xpip-mirror:
	pip3 install --upgrade xkits tabulate wcwidth ping3 toml pip
	python3 setup-mirror.py check sdist bdist_wheel --universal
build-xpip-upload:
	pip3 install --upgrade wheel packaging twine keyring keyrings.alt
	python3 setup-upload.py check sdist bdist_wheel --universal
build-xpip-build:
	pip3 install --upgrade "setuptools >= 69.3.0, <= 70.3.0"
	python3 setup-build.py check sdist bdist_wheel --universal
build: build-clean build-xpip-mirror build-xpip-upload build-xpip-build


install-xpip-mirror:
	pip3 install --force-reinstall --no-deps dist/xpip_mirror-*.whl
install-xpip-upload:
	pip3 install --force-reinstall --no-deps dist/xpip_upload-*.whl
install-xpip-build:
	pip3 install --force-reinstall --no-deps dist/xpip_build-*.whl
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
	pip3 install --upgrade pylint flake8 pytest pytest-cov
pylint-xpip-mirror:
	pylint $$(git ls-files xpip_mirror/*.py)
pylint-xpip-upload:
	pylint $$(git ls-files xpip_upload/*.py)
pylint-xpip-build:
	pylint $$(git ls-files xpip_build/*.py)
pylint: pylint-xpip-mirror pylint-xpip-upload pylint-xpip-build
flake8:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
pytest-xpip-mirror:
	pytest --cov=xpip_mirror --cov-report=term-missing --cov-report=xml --cov-report=html --cov-config=.coveragerc --cov-fail-under=100
pytest-xpip-upload:
	pytest --cov=xpip_upload --cov-report=term-missing --cov-report=xml --cov-report=html --cov-config=.coveragerc --cov-fail-under=100
pytest-xpip-build:
	pytest --cov=xpip_build --cov-report=term-missing --cov-report=xml --cov-report=html --cov-config=.coveragerc --cov-fail-under=100
pytest: pytest-xpip-mirror pytest-xpip-upload pytest-xpip-build
pytest-clean:
	rm -rf .pytest_cache
test-xpip-mirror: prepare-test pylint-xpip-mirror flake8 pytest-xpip-mirror
test-xpip-upload: prepare-test pylint-xpip-upload flake8 pytest-xpip-upload
test-xpip-build: prepare-test pylint-xpip-build flake8 pytest-xpip-build
test: prepare-test pylint flake8 pytest
test-clean: pytest-clean
