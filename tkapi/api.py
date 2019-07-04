import urllib
import requests
from typing import List

from tkapi.fractie import Fractie, FractieZetel
from tkapi.persoon import Persoon
from .activiteit import Activiteit
from .agendapunt import Agendapunt
from .besluit import Besluit
from .commissie import Commissie
from .document import Document
from .dossier import Dossier
from .kamervraag import Kamervraag, Antwoord
from .persoon import PersoonGeschenk
from .persoon import PersoonReis
from .stemming import Stemming
from .vergadering import Vergadering
from .document import VerslagAlgemeenOverleg
from .zaak import Zaak

from .filter import VerwijderdFilter


class Api(object):
    _user = None
    _password = None
    _verbose = False
    _max_items_per_page = 250
    api_root = 'https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/'

    def __init__(self, user=None, password=None, api_root=None, verbose=None):
        if user is not None:
            Api._user = user
        if password is not None:
            Api._password = password
        if api_root is not None:
            Api.api_root = api_root
        if verbose is not None:
            Api._verbose = verbose

    @classmethod
    def get_commissies(cls, filter=None, order=None, max_items=None) -> List[Commissie]:
        return cls.get_items(Commissie, filter, order, max_items)

    @classmethod
    def get_personen(cls, filter=None, order=None, max_items=None) -> List[Persoon]:
        return cls.get_items(Persoon, filter, order, max_items)

    @classmethod
    def get_fracties(cls, filter=None, order=None, max_items=None) -> List[Fractie]:
        return cls.get_items(Fractie, filter, order, max_items)

    @classmethod
    def get_vergaderingen(cls, filter=None, order=None, max_items=None) -> List[Vergadering]:
        return cls.get_items(Vergadering, filter, order, max_items)

    @classmethod
    def get_verslagen_van_algemeen_overleg(cls, filter=None, order=None, max_items=None) -> List[VerslagAlgemeenOverleg]:
        return cls.get_items(VerslagAlgemeenOverleg, filter, order, max_items)

    @classmethod
    def get_kamervragen(cls, filter=None, order=None, max_items=None) -> List[Kamervraag]:
        return cls.get_items(Kamervraag, filter, order, max_items)

    @classmethod
    def get_antwoorden(cls, filter=None, order=None, max_items=None) -> List[Antwoord]:
        return cls.get_items(Antwoord, filter, order, max_items)

    @classmethod
    def get_documenten(cls, filter=None, order=None, max_items=None) -> List[Document]:
        return cls.get_items(Document, filter, order, max_items)

    @classmethod
    def get_dossiers(cls, filter=None, order=None, max_items=None) -> List[Dossier]:
        return cls.get_items(Dossier, filter, order, max_items)

    @classmethod
    def get_zaken(cls, filter=None, order=None, max_items=None) -> List[Zaak]:
        return cls.get_items(Zaak, filter, order, max_items)

    @classmethod
    def get_activiteiten(cls, filter, order=None, max_items=None) -> List[Commissie]:
        return cls.get_items(Activiteit, filter, order, max_items)

    @classmethod
    def get_stemmingen(cls, filter=None, order=None, max_items=None) -> List[Stemming]:
        return cls.get_items(Stemming, filter, order, max_items)

    @classmethod
    def get_agendapunten(cls, filter=None, order=None, max_items=None) -> List[Agendapunt]:
        return cls.get_items(Agendapunt, filter, order, max_items)

    @classmethod
    def get_besluiten(cls, filter=None, order=None, max_items=None) -> List[Besluit]:
        return cls.get_items(Besluit, filter, order, max_items)

    @classmethod
    def get_fractie_zetels(cls, filter=None, order=None, max_items=None) -> List[FractieZetel]:
        return cls.get_items(FractieZetel, filter, order, max_items)

    @classmethod
    def get_reizen(cls, filter=None, order=None, max_items=None) -> List[PersoonReis]:
        return cls.get_items(PersoonReis, filter, order, max_items)

    @classmethod
    def get_geschenken(cls, filter=None, order=None, max_items=None) -> List[PersoonGeschenk]:
        return cls.get_items(PersoonGeschenk, filter, order, max_items)

    @staticmethod
    def add_filter_to_params(filter, params):
        if filter is None:
            return params
        if '$filter' in params and params['$filter']:
            params['$filter'] += ' and '
        else:
            params['$filter'] = ''
        params['$filter'] += filter.filter_str
        return params

    @staticmethod
    def add_non_deleted_filter(params):
        non_deleted_filter = VerwijderdFilter()
        non_deleted_filter.filter_verwijderd()
        return Api.add_filter_to_params(non_deleted_filter, params)

    @classmethod
    def get_all_items(cls, page, max_items=None):
        items = []
        for item in page['value']:
            items.append(item)
            if max_items is not None and len(items) >= max_items:
                return items
        while '@odata.nextLink' in page:
            page = cls.request_json(page['@odata.nextLink'])
            for item in page['value']:
                items.append(item)
                if max_items is not None and len(items) >= max_items:
                    return items
        return items

    @classmethod
    def request_json(cls, url, params=None, max_items=None):
        url = url.strip()
        if not params:
            params = {}
        if '$format' not in url:
            params['$format'] = 'application/json;odata.metadata=full',
        if max_items is not None:
            params['$top'] = max_items,
        if cls.api_root.strip().lower() not in url.lower():
            url = cls.api_root + url
        response = requests.get(
            url=url,
            params=params,
            auth=(str(cls._user), str(cls._password)),
            timeout=60
        )
        if cls._verbose:
            print('url: ', urllib.parse.unquote(response.url))
        if response.status_code in [204, 404, 500]:
            print('HTTP STATUS CODE', response.status_code)
            print('### WARNING: requested item does not exist:', url, '###')
            return {}
        elif response.status_code != 200:
            print('HTTP STATUS CODE', response.status_code)
            print('ODATA ERROR: ', response.json()['error']['message'])
        # assert response.status_code == 200
        return response.json()

    @classmethod
    def get_item(cls, tkitem, id, params=None):
        url = tkitem.url + '('+ id + ')'
        if params is None:
            params = tkitem.get_param_expand()
        return tkitem(cls.request_json(url, params))

    @classmethod
    def get_related(cls, tkitem_related, related_url, filter=None, params=None):
        if params is None:
            params = tkitem_related.get_param_expand()
        params = Api.add_filter_to_params(filter, params)
        first_page = cls.request_json(related_url, params)
        related_items = []
        if 'value' in first_page:
            items_json = cls.get_all_items(first_page)
            for item_json in items_json:
                related_items.append(tkitem_related(item_json))
        elif first_page:
            related_items.append(tkitem_related(first_page))
        return related_items

    @classmethod
    def get_items(cls, item_class, filter=None, order=None, max_items=None):
        items = []
        params = cls.create_query_params(tkitem_class=item_class, filter=filter, order=order)
        max_items_request = max_items if max_items is not None and max_items <= cls._max_items_per_page else None
        first_page = cls.request_json(item_class.url, params, max_items=max_items_request)
        items_json = cls.get_all_items(first_page, max_items=max_items)
        for item_json in items_json:
            item = item_class(item_json)
            items.append(item)
        return items

    @staticmethod
    def create_query_params(tkitem_class, filter=None, order=None):
        params = tkitem_class.get_params_default()
        params = Api.add_filter_to_params(filter, params)
        params = Api.add_non_deleted_filter(params)
        if tkitem_class.filter_param:
            if params['$filter']:
                params['$filter'] += ' and '
            params['$filter'] += tkitem_class.filter_param
        if order:
            params['$orderby'] = order.order_by_str
        return params
