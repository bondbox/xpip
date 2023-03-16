#!/usr/bin/bash
pushd `dirname $0`
pushd ../../

rm -rf "build"
rm -rf "dist"
rm -rf "*.egg-info"

python3 setup.py check
python3 setup.py sdist
python3 setup.py bdist_wheel --universal

popd
popd
