import requests

from .agendapunt import Agendapunt
from .besluit import Besluit
from .commissie import Commissie
from .document import ParlementairDocument
from .dossier import Dossier
from .kamerstuk import Kamerstuk
from .activiteit import Activiteit
from .kamervraag import Kamervraag, Antwoord
from .persoon import Persoon
from .stemming import Stemming
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
        params['$filter'] = ''
        if filter is not None:
            params['$filter'] += filter.filter_str
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
        # params['$format'] = 'json',
        params['$format'] = 'application/json;odata=fullmetadata',
        # print(params)
        r = requests.get(Api.API_ROOT_URL + url, params=params, auth=(self._user, self._password))
        if self._verbose:
            print('url: ' + str(r.url))
        if r.status_code != 200:
            print(r.text)
        assert r.status_code == 200
        return r.json()

    def get_item(self, tkitem, id, params=None):
        url = tkitem.url + '(guid\'' + id + '\')'
        if params is None:
            params = tkitem.get_param_expand()
        return tkitem(self.request_json(url, params))

    def get_items(self, item_class, filter=None, max_items=None):
        items = []
        params = item_class.get_params_default()
        params = Api.add_filter_to_params(filter, params)
        if item_class.filter_param:
            if params['$filter']:
                params['$filter'] += ' and '
            params['$filter'] += item_class.filter_param
        # print(params)
        first_page = self.request_json(item_class.url, params)
        items_json = self.get_all_items(first_page, max_items=max_items)
        for item_json in items_json:
            item = item_class(item_json)
            items.append(item)
        return items

    def get_commissies(self, filter=None, max_items=None):
        return self.get_items(Commissie, filter, max_items)

    def get_personen(self, max_items=None):
        return self.get_items(Persoon, filter=None, max_items=max_items)

    def get_verslagen_van_algemeen_overleg(self, filter=None, max_items=None):
        return self.get_items(VerslagAlgemeenOverleg, filter=filter, max_items=max_items)

    def get_kamervragen(self, filter=None, max_items=None):
        return self.get_items(Kamervraag, filter, max_items)

    def get_antwoorden(self, filter=None, max_items=None):
        return self.get_items(Antwoord, filter, max_items)

    def get_parlementaire_documenten(self, filter=None):
        return self.get_items(ParlementairDocument, filter, max_items=None)

    def get_dossiers(self, filter=None, max_items=None):
        return self.get_items(Dossier, filter, max_items)

    def get_zaken(self, filter=None):
        return self.get_items(Zaak, filter, max_items=None)

    def get_activiteiten(self, filter, max_items=None):
        return self.get_items(Activiteit, filter=filter, max_items=max_items)

    def get_kamerstukken(self, filter=None, max_items=None):
        return self.get_items(Kamerstuk, filter, max_items)

    def get_stemmingen(self, filter=None, max_items=None):
        return self.get_items(Stemming, filter, max_items)

    def get_agendapunten(self, filter=None, max_items=None):
        return self.get_items(Agendapunt, filter, max_items)

    def get_besluiten(self, filter=None, max_items=None):
        return self.get_items(Besluit, filter, max_items)
