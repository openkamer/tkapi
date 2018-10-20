# tkapi
[![PyPI version](https://badge.fury.io/py/tkapi.svg)](https://badge.fury.io/py/tkapi)  
Python bindings for the [Tweede Kamer](https://tweedekamer.nl) [Open Data Portaal](https://opendata.tweedekamer.nl) OData API.

Requires Python 3.3+

**WARNING**: This is a work in progress. Code is not clean, nor complete. There will be major changes that break everything!

You are welcome to open an issue if you have any problems, questions or suggestions.

## Installation
```
pip install tkapi
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

Where `USERNAME` and `PASSWORD` are your Tweede Kamer OpenData username and password. 
You can get one by registering at https://opendata.tweedekamer.nl.

The tests can serve as more detailed examples.

## Entities
**Bold** entities are implemented.

|                            |                            |                              |
|----------------------------|----------------------------|------------------------------|
| **Activiteit**             | **Commissie**              | **Persoon**                  |
| ActiviteitActor            | CommissieOrganisatie       | PersoonAdres                 |
| **Zaak**                   | CommissieAanvullendGegeven | PersoonContactinformatie     |
| ZaakActor                  | **CommissieZetel**         | PersoonGeschenk              |
| **Kamerstukdossier**       | **CommissieVastPersoon**   | PersoonLoopbaan              |
| **Fractie**                | CommissieVastVacature      | PersoonNevenfunctie          |
| FractieOrganisatie         | CommissieVervangerVacature | PersoonNevenfunctieInkomsten |
| FractieAanvullendGegeven   | CommissieVervangerPersoon  | PersoonOnderwijs             |
| **FractieLid**             |                            | **PersoonReis**              |
| **Stemming**               |                            | PersoonFunctie               |
| Zaal                       |                            |                              |
| Reservering                |                            |                              |
| **Vergadering**            |                            |                              |
| **ParlementairDocument**   |                            |                              |
| ParlementairDocumentVersie |                            |                              |
| Bestand                    |                            |                              |
| **Kamerstuk**              |                            |                              |
| **Verslag**                |                            |                              |
| **Agendapunt**             |                            |                              |
| **Besluit**                |                            |                              |

## Development

### Tests

Run all tests,
```bash
python -m unittest discover
```

#### Coverage report

Run all tests,
```bash
coverage -m unittest discover
```

Create coverage report,
```bash
coverage html
```
Then visit htmlcov/index.html in your browser.
