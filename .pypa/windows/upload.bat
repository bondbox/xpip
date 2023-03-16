pushd %~dp0
pushd ..\..\

python -m twine check dist/*
python -m twine upload dist/*

popd
popd

pause
