# tkapi
[![PyPI version](https://badge.fury.io/py/tkapi.svg)](https://badge.fury.io/py/tkapi)  
Python bindings for the [Tweede Kamer](https://tweedekamer.nl) [Open Data Portaal](https://opendata.tweedekamer.nl) OData API.

Requires Python 3.5+

You are welcome to open an issue if you have any problems, questions or suggestions.

## Installation
```
pip install tkapi
```

## Authentication
You need to whitelist your IP by registering at https://opendata.tweedekamer.nl.

## Usage
A simple first example,
```python
import tkapi

api = tkapi.Api()
personen = api.get_personen(max_items=100)
for persoon in personen:
    print(persoon.achternaam)
```

For more examples see the `examples` directory and the tests.

## Entities
Implemented:

| Algemeen                   | Commissie                  | Persoon                      |
|----------------------------|----------------------------|------------------------------|
| **Activiteit**             | **Commissie**              | **Persoon**                  |
| **Zaak**                   | **CommissieZetel**         | **PersoonGeschenk**          |
| **Kamerstukdossier**       | **CommissieVastPersoon**   | **PersoonLoopbaan**          |
| **Fractie**                | **CommissieVervangerPersoon** | **PersoonNevenfunctie**      |
| **FractieZetel**           |                            | **PersoonNevenfunctieInkomsten** |
| **Stemming**               |                            | **PersoonOnderwijs**         |
| **Vergadering**            |                            | **PersoonReis**              |
| **Document**               |                            | **PersoonFunctie**           |
| **Agendapunt**             |                            |                              |
| **Besluit**                |                            |                              |
| **Verslag**                |                            |                              |

TODO:

| Algemeen                   | Commissie                  | Persoon                      |
|----------------------------|----------------------------|------------------------------|
| ActiviteitActor            | CommissieVastVacature      | PersoonAdres                 |
| ZaakActor                  | CommissieVervangerVacature | PersoonContactinformatie     |
| FractieAanvullendGegeven   |                            |                              |
| Zaal                       |                            |                              |
| Reservering                |                            |                              |
| DocumentVersie             |                            |                              |

## Development

### Tests

Run all tests,
```bash
python -m unittest discover
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
