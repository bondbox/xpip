MAKEFLAGS += --always-make

VERSION := $(shell python3 setup.py --version)

all: build reinstall test


version:
	@echo ${VERSION}


clean-cover:
	rm -rf cover .coverage coverage.xml htmlcov
clean-tox:
	rm -rf .stestr .tox
clean: build-clean test-clean clean-cover clean-tox


upload:
	python3 -m twine check dist/xpip_upload-*
	python3 -m twine upload --verbose --config-file .pypirc --repository xpip-upload dist/xpip_upload-*


build-prepare:
	python3 -m pip install --upgrade setuptools wheel packaging twine keyring keyrings.alt
build-clean:
	rm -rf build dist *.egg-info htmlcov coverage.xml .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
build: build-prepare build-clean
	python3 setup.py check sdist bdist_wheel --universal


install:
	python3 -m pip install --force-reinstall --no-deps dist/*.whl
uninstall:
	python3 -m pip uninstall -y xpip-upload
reinstall: uninstall install


test-prepare:
	python3 -m pip install --upgrade mock pylint flake8 pytest pytest-cov
pylint:
	pylint $(shell git ls-files xpip_upload/*.py)
flake8:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
pytest:
	pytest --cov=xpip_upload --cov-report=term-missing --cov-report=xml --cov-report=html --cov-config=.coveragerc --cov-fail-under=100 xpip_upload/unittest/*.py
pytest-clean:
	rm -rf .pytest_cache
test: test-prepare pylint flake8 pytest
test-clean: pytest-clean
