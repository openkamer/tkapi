import requests

from .commissie import Commissie
from .kamervraag import KamerVraag, Antwoord
from .persoon import Persoon
from .verslag import VerslagAlgemeenOverleg


class Api(object):
    API_ROOT_URL = 'https://gegevensmagazijn.tweedekamer.nl/OData/v1/'

    def __init__(self, user, password):
        self._user = user
        self._password = password

    def get_all_items(self, page, max_items=None):
        items = []
        for item in page['value']:
            items.append(item)
        while 'odata.nextLink' in page:
            page = self.request_json(page['odata.nextLink'])
            for item in page['value']:
                items.append(item)
                if max_items and len(items) >= max_items:
                    return items
        return items

    def request_json(self, url, params=None, verbose=False):
        if not params:
            params = {}
        params['$format'] = 'json',
        r = requests.get(Api.API_ROOT_URL + url, params=params, auth=(self._user, self._password))
        if verbose:
            print('url: ' + str(r.url))
        if r.status_code != 200:
            print(r.text)
        assert r.status_code == 200
        return r.json()

    def get_commissies(self, max_items=None):
        commissies = []
        page = self.request_json(Commissie.url, Commissie.params_default)
        commissie_items = self.get_all_items(page, max_items=max_items)
        for item in commissie_items:
            commissies.append(Commissie(item))
        return commissies

    def get_kamervragen(self, start_datetime, end_datetime):
        first_page = self.request_json(KamerVraag.url, KamerVraag.params(start_datetime, end_datetime))
        items = self.get_all_items(first_page)
        vragen = []
        for item in items:
            vraag = KamerVraag(item)
            vragen.append(vraag)
            print('create vraag for date: ' + str(vraag.datum))
        return vragen

    def get_schriftelijke_vraag_json(self, id):
        url = 'ParlementairDocument(guid\'' + id + '\')'
        params = {
            '$expand': 'Zaak',
        }
        return self.request_json(url, params)

    def get_antwoorden(self, start_datetime, end_datetime):
        first_page = self.request_json(Antwoord.url, Antwoord.params(start_datetime, end_datetime))
        items = self.get_all_items(first_page)
        antwoorden = []
        for item in items:
            antwoord = Antwoord(item)
            print('create antwoord for date: ' + str(antwoord.datum))
            antwoorden.append(antwoord)
        return antwoorden

    def get_personen(self, require_surname=True, max_items=None):
        personen = []
        page = self.request_json(Persoon.url, Persoon.params(require_surname=True))
        commissie_items = self.get_all_items(page, max_items=max_items)
        for item in commissie_items:
            personen.append(Persoon(item))
        return personen

    def get_verslagen_van_algemeen_overleg(self, start_datetime, end_datetime):
        verslagen = []
        first_page = self.request_json(VerslagAlgemeenOverleg.url, VerslagAlgemeenOverleg.params(start_datetime, end_datetime))
        items = self.get_all_items(first_page)
        for item in items:
            verslag = VerslagAlgemeenOverleg(item)
            verslagen.append(verslag)
            print(verslag.datum)
        return verslagen
