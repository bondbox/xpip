#!/usr/bin/bash
pushd `dirname $0`
pushd ../../

rm -rf "build"
rm -rf "dist"
rm -rf "*.egg-info"

rm -rf setup.py
cp setuptools/xpip-mirror.py setup.py

python3 setup.py check
python3 setup.py sdist
python3 setup.py bdist_wheel --universal

rm -rf setup.py
popd
popd
