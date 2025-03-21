set -e
set -x

pip3 install --break-system-packages setuptools xkits tabulate wcwidth ping3 toml pip wheel packaging twine keyring keyrings.alt
python3 setup-mirror.py check bdist_wheel --universal
python3 setup-upload.py check bdist_wheel --universal
python3 setup-build.py check bdist_wheel --universal


pip3 install --break-system-package --force-reinstall --no-deps dist/xpip_mirror-*.whl
pip3 install --break-system-package --force-reinstall --no-deps dist/xpip_upload-*.whl
pip3 install --break-system-package --force-reinstall --no-deps dist/xpip_build-*.whl


pip3 install --break-system-packages pylint flake8 pytest pytest-cov

pylint $(git ls-files xpip_mirror/*.py)
pylint $(git ls-files xpip_upload/*.py)
pylint $(git ls-files xpip_build/*.py)

flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

pytest --cov=xpip_mirror --cov-report=term-missing --cov-report=xml --cov-report=html --cov-config=.coveragerc --cov-fail-under=100 xpip_mirror/unittest/*.py
pytest --cov=xpip_upload --cov-report=term-missing --cov-report=xml --cov-report=html --cov-config=.coveragerc --cov-fail-under=100 xpip_upload/unittest/*.py
pytest --cov=xpip_build --cov-report=term-missing --cov-report=xml --cov-report=html --cov-config=.coveragerc --cov-fail-under=100 xpip_build/unittest/*.py
