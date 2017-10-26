import requests

from .commissie import Commissie
from .document import ParlementairDocument
from .dossier import Dossier
from .activiteit import Activiteit
from .kamervraag import KamerVraag, Antwoord
from .persoon import Persoon
from .verslag import VerslagAlgemeenOverleg
from .zaak import Zaak


class Api(object):
    API_ROOT_URL = 'https://gegevensmagazijn.tweedekamer.nl/OData/v1/'

    def __init__(self, user, password, verbose=False):
        self._user = user
        self._password = password
        self._verbose = verbose

    @staticmethod
    def add_filter_to_params(filter, params):
        if not filter:
            return
        params['$filter'] = filter.filter_str
        return params

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

    def request_json(self, url, params=None):
        if not params:
            params = {}
        params['$format'] = 'json',
        # params['$format'] = 'application/json;odata=fullmetadata',
        r = requests.get(Api.API_ROOT_URL + url, params=params, auth=(self._user, self._password))
        if self._verbose:
            print('url: ' + str(r.url))
        if r.status_code != 200:
            print(r.text)
        assert r.status_code == 200
        return r.json()

    def get_item(self, tkitem, id, params):
        url = tkitem.url + '(guid\'' + id + '\')'
        return tkitem(self.request_json(url, params))

    def get_commissies(self, max_items=None):
        commissies = []
        page = self.request_json(Commissie.url, Commissie.get_params_default())
        commissie_items = self.get_all_items(page, max_items=max_items)
        for item in commissie_items:
            commissies.append(Commissie(item))
        return commissies

    def get_kamervragen(self, start_datetime, end_datetime):
        first_page = self.request_json(KamerVraag.url, KamerVraag.get_params_default(start_datetime, end_datetime))
        items = self.get_all_items(first_page)
        vragen = []
        for item in items:
            vraag = KamerVraag(item)
            vragen.append(vraag)
            print('create vraag for date: ' + str(vraag.datum))
        return vragen

    def get_antwoorden(self, start_datetime, end_datetime):
        first_page = self.request_json(Antwoord.url, Antwoord.get_params_default(start_datetime, end_datetime))
        items = self.get_all_items(first_page)
        antwoorden = []
        for item in items:
            antwoord = Antwoord(item)
            print('create antwoord for date: ' + str(antwoord.datum))
            antwoorden.append(antwoord)
        return antwoorden

    def get_personen(self, require_surname=True, max_items=None):
        personen = []
        page = self.request_json(Persoon.url, Persoon.get_params_default(require_surname=True))
        commissie_items = self.get_all_items(page, max_items=max_items)
        for item in commissie_items:
            personen.append(Persoon(item))
        return personen

    def get_parlementaire_documenten(self, filter=None):
        documenten = []
        params = ParlementairDocument.get_params_default()
        params = Api.add_filter_to_params(filter, params)
        first_page = self.request_json(ParlementairDocument.url, params)
        items = self.get_all_items(first_page)
        for item in items:
            document = ParlementairDocument(item)
            documenten.append(document)
        return documenten

    def get_verslagen_van_algemeen_overleg(self, start_datetime, end_datetime):
        verslagen = []
        first_page = self.request_json(VerslagAlgemeenOverleg.url, VerslagAlgemeenOverleg.get_params_default(start_datetime, end_datetime))
        items = self.get_all_items(first_page)
        for item in items:
            verslag = VerslagAlgemeenOverleg(item)
            verslagen.append(verslag)
            print(verslag.datum)
        return verslagen

    def get_dossiers(self, filter=None, max_items=None):
        dossiers = []
        params = Dossier.get_params_default()
        params = Api.add_filter_to_params(filter, params)
        first_page = self.request_json(Dossier.url, params)
        items = self.get_all_items(first_page, max_items=max_items)
        for item in items:
            dossier = Dossier(item)
            dossiers.append(dossier)
        return dossiers

    def get_zaken(self, filter=None):
        zaken = []
        params = Zaak.get_params_default()
        params = Api.add_filter_to_params(filter, params)
        first_page = self.request_json(Zaak.url, params)
        items = self.get_all_items(first_page)
        for item in items:
            zaak = Zaak(item)
            zaken.append(zaak)
        return zaken

    def get_zaak(self, onderwerp):
        first_page = self.request_json(Zaak.url, Zaak.filter_onderwerp(onderwerp))
        items = self.get_all_items(first_page)
        if items:
            return Zaak(items[0])
        return None

    def get_activiteiten(self, max_items=None):
        activiteiten = []
        params = Activiteit.get_params_default()
        # params['$filter'] = filter.filter_str
        first_page = self.request_json(Activiteit.url, params)
        items = self.get_all_items(first_page, max_items=max_items)
        for item in items:
            activiteit = Activiteit(item)
            activiteiten.append(activiteit)
        return activiteiten
