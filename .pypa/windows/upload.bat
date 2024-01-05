pushd %~dp0
pushd ..\..\

python -m twine check dist/*
python -m twine upload --verbose --config-file .pypirc --repository xpip-python dist/*

popd
popd

pause
