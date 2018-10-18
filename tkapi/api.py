import requests

from .actor import Fractie, Persoon, FractieLid
from .agendapunt import Agendapunt
from .besluit import Besluit
from .commissie import Commissie
from .document import ParlementairDocument
from .dossier import Dossier
from .kamerstuk import Kamerstuk
from .activiteit import Activiteit
from .kamervraag import Kamervraag, Antwoord
from .stemming import Stemming
from .verslag import VerslagAlgemeenOverleg
from .zaak import Zaak


class Api(object):
    _user = None
    _password = None
    _verbose = False
    api_root = 'https://gegevensmagazijn.tweedekamer.nl/OData/v3/1.0/'

    def __init__(self, user=None, password=None, api_root=None, verbose=None):
        if user is not None:
            self._user = user
        if password is not None:
            self._password = password
        if api_root is not None:
            self.api_root = api_root
        if verbose is not None:
            self._verbose = verbose

    @classmethod
    def get_commissies(cls, filter=None, max_items=None):
        return cls.get_items(Commissie, filter, max_items)

    @classmethod
    def get_personen(cls, max_items=None):
        return cls.get_items(Persoon, filter=None, max_items=max_items)

    @classmethod
    def get_fracties(cls, filter=None, max_items=None):
        return cls.get_items(Fractie, filter, max_items)

    @classmethod
    def get_verslagen_van_algemeen_overleg(cls, filter=None, max_items=None):
        return cls.get_items(VerslagAlgemeenOverleg, filter=filter, max_items=max_items)

    @classmethod
    def get_kamervragen(cls, filter=None, max_items=None):
        return cls.get_items(Kamervraag, filter, max_items)

    @classmethod
    def get_antwoorden(cls, filter=None, max_items=None):
        return cls.get_items(Antwoord, filter, max_items)

    @classmethod
    def get_parlementaire_documenten(cls, filter=None, max_items=None):
        return cls.get_items(ParlementairDocument, filter, max_items=max_items)

    @classmethod
    def get_dossiers(cls, filter=None, max_items=None):
        return cls.get_items(Dossier, filter, max_items)

    @classmethod
    def get_zaken(cls, filter=None):
        return cls.get_items(Zaak, filter, max_items=None)

    @classmethod
    def get_activiteiten(cls, filter, max_items=None):
        return cls.get_items(Activiteit, filter=filter, max_items=max_items)

    @classmethod
    def get_kamerstukken(cls, filter=None, max_items=None):
        return cls.get_items(Kamerstuk, filter, max_items)

    @classmethod
    def get_stemmingen(cls, filter=None, max_items=None):
        return cls.get_items(Stemming, filter, max_items)

    @classmethod
    def get_agendapunten(cls, filter=None, max_items=None):
        return cls.get_items(Agendapunt, filter, max_items)

    @classmethod
    def get_besluiten(cls, filter=None, max_items=None):
        return cls.get_items(Besluit, filter, max_items)

    @classmethod
    def get_fractie_leden(cls, filter=None, max_items=None):
        return cls.get_items(FractieLid, filter, max_items)

    @staticmethod
    def add_filter_to_params(filter, params):
        params['$filter'] = ''
        if filter is not None:
            params['$filter'] += filter.filter_str
        return params

    @classmethod
    def get_all_items(cls, page, max_items=None):
        items = []
        for item in page['value']:
            items.append(item)
            if max_items is not None and len(items) >= max_items:
                return items
        while 'odata.nextLink' in page:
            page = cls.request_json(page['odata.nextLink'])
            for item in page['value']:
                items.append(item)
                if max_items is not None and len(items) >= max_items:
                    return items
        return items

    @classmethod
    def request_json(cls, url, params=None):
        if not params:
            params = {}
        # params['$format'] = 'json',
        params['$format'] = 'application/json;odata=fullmetadata',
        response = requests.get(cls.api_root + url, params=params, auth=(cls._user, cls._password))
        if cls._verbose:
            print('url: ' + str(response.url))
        if response.status_code == 204:
            print('### WARNING: requested item does not exist:', url, '###')
            return {}
        elif response.status_code != 200:
            print(response.status_code)
        assert response.status_code == 200
        return response.json()

    @classmethod
    def get_item(cls, tkitem, id, params=None):
        url = tkitem.url + '(guid\'' + id + '\')'
        if params is None:
            params = tkitem.get_param_expand()
        return tkitem(cls.request_json(url, params))

    @classmethod
    def get_related(cls, tkitem_related, related_url, filter=None, params=None):
        if params is None:
            params = tkitem_related.get_param_expand()
        params = Api.add_filter_to_params(filter, params)
        related_json = cls.request_json(related_url, params)
        related_items = []
        if 'value' in related_json:
            for item_json in related_json['value']:
                related_items.append(tkitem_related(item_json))
        elif related_json:
            related_items.append(tkitem_related(related_json))
        return related_items

    @classmethod
    def get_items(cls, item_class, filter=None, max_items=None):
        items = []
        params = item_class.get_params_default()
        params = Api.add_filter_to_params(filter, params)
        if item_class.filter_param:
            if params['$filter']:
                params['$filter'] += ' and '
            params['$filter'] += item_class.filter_param
        first_page = cls.request_json(item_class.url, params)
        items_json = cls.get_all_items(first_page, max_items=max_items)
        for item_json in items_json:
            item = item_class(item_json)
            items.append(item)
        return items
