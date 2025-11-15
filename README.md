# tkapi
[![PyPI version](https://badge.fury.io/py/tkapi.svg)](https://badge.fury.io/py/tkapi) ![CI/CD status](https://github.com/openkamer/tkapi/actions/workflows/main.yml/badge.svg)  
Python ORM and bindings for the [Tweede Kamer](https://tweedekamer.nl) [Open Data Portaal](https://opendata.tweedekamer.nl) OData API.

A pure Python interface for the Tweede Kamer API with type annotations for easy data model discovery.

Requires Python 3.5+.

Please create an issue if you have any problems, questions or suggestions.

## Installation
```
pip install tkapi
```

## Data model
See [Open Kamer Data Model documentation](https://opendata.tweedekamer.nl/documentatie/informatiemodel) for the data model that is mapped to Python classes.

## Usage
A simple first example,
```python
import tkapi

api = tkapi.TKApi()
personen = api.get_personen(max_items=100)
for persoon in personen:
    print(persoon.achternaam)
```

For more examples see the [examples](./examples) and [tests](./tests).

## Entities

See Tweede Kamer [documentation](https://opendata.tweedekamer.nl/documentatie/informatiemodel-20) for details.

| Algemeen                    | Persoon                       | Fractie                  | Commissie                       |
|-----------------------------|-------------------------------|--------------------------|---------------------------------|
| Activiteit                  | Persoon                       | Fractie                  | Commissie                       |
| ActiviteitActor             | PersoonContactinformatie      | FractieZetel             | CommissieContactinformatie      |
| Agendapunt                  | PersoonFunctie                | FractieZetelPersoon      | CommissieZetel                  |
| Besluit                     | PersoonGeschenk               | FractieZetelVacature     | CommissieZetelVastPersoon       |
| Document                    | PersoonLoopbaan               | FractieZetelVacature     | CommissieZetelVastVacature      |
| DocumentActor               | PersoonNevenfunctie           |                          | CommissieZetelVervangerPersoon  |
| DocumentVersie              | PersoonNevenfunctieInkomsten  |                          | CommissieZetelVervangerVacature |
| Kamerstukdossier            | PersoonOnderwijs              |                          |                                 |
| Reservering                 | PersoonReis                   |                          |                                 |
| Stemming                    |                               |                          |                                 |
| Vergadering                 |                               |                          |                                 |
| Verslag                     |                               |                          |                                 |
| Zaak                        |                               |                          |                                 |
| ZaakActor                   |                               |                          |                                 |
| Zaal                        |                               |                          |                                 |

## Development

### Tests

Run all tests,
```bash
pytest
```

#### Coverage report

Run all tests,
```bash
coverage run -m unittest discover
```

Create coverage report,
```bash
coverage html
```
Then visit htmlcov/index.html in your browser.

### Publishing

This project uses Python packaging with `pyproject.toml`. To publish a new version to PyPI:

1. **Install build tools** (if not already installed):
   ```bash
   pip install build twine
   ```

2. **Update the version** in `pyproject.toml`:
   ```toml
   version = "X.Y.Z"
   ```

3. **Build the package**:
   ```bash
   python -m build
   ```
   This will create distribution files in the `dist/` directory.

4. **Test the build locally** (optional but recommended):
   ```bash
   pip install dist/tkapi-X.Y.Z-py3-none-any.whl
   ```

5. **Upload to Test PyPI** (optional, for testing):
   ```bash
   twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   ```

6. **Upload to PyPI**:
   ```bash
   twine upload dist/*
   ```
   You'll need PyPI credentials (username and password/token). You can create an API token at https://pypi.org/manage/account/token/
