# Howto create PyPi release

Install setuptools, wheel and twine:
```
python -m pip install --upgrade setuptools wheel twine
```

Increase the version number in `setup.py`.

Create dist:
```
python setup.py sdist bdist_wheel
```

Upload:
```
twine upload dist/*
```
