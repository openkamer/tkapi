# tkapi

Python bindings for the Tweede Kamer OData API.

Requires Python 3.3+

WARNING: This is a work in progress. There will be major changes that break everything!

## Installation
```
$ pip install tkapi
```

## Usage
A simple first example,
```python
import tkapi

api = tkapi.Api(user=USERNAME, password=PASSWORD)
personen = api.get_personen(max_items=100)
for persoon in personen:
    print(persoon.achternaam)
```

Where `USERNAME` and `PASSWORD` are your Tweede Kamer OpenData username and password. You can get one by registering at https://opendata.tweedekamer.nl .

## Tests

Run all tests,
```
$ python -m unittest discover
```
