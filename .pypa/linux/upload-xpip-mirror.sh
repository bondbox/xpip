#!/usr/bin/bash
pushd `dirname $0`
pushd ../../

python3 -m twine check dist/*
python3 -m twine upload --verbose --config-file .pypirc --repository xpip-mirror dist/*

popd
popd
