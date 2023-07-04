# tkapi
[![PyPI version](https://badge.fury.io/py/tkapi.svg)](https://badge.fury.io/py/tkapi)  
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
| ActiviteitActor             | PersoonContactinformatie      | FractieAanvullendGegeven | CommissieContactinformatie      |
| Agendapunt                  | PersoonFunctie                | FractieZetel             | CommissieZetel                  |
| Besluit                     | PersoonGeschenk               | FractieZetelPersoon      | CommissieZetelVastPersoon       |
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
