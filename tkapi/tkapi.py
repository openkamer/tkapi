import logging
import urllib.parse
import requests
from typing import List

from tkapi.activiteit import Activiteit
from tkapi.agendapunt import Agendapunt
from tkapi.besluit import Besluit
from tkapi.commissie import Commissie
from tkapi.document import Document
from tkapi.document import VerslagAlgemeenOverleg
from tkapi.dossier import Dossier
from tkapi.fractie import Fractie
from tkapi.fractie import FractieZetel
from tkapi.kamervraag import Kamervraag
from tkapi.kamervraag import Antwoord
from tkapi.persoon import Persoon
from tkapi.persoon import PersoonGeschenk
from tkapi.persoon import PersoonReis
from tkapi.stemming import Stemming
from tkapi.vergadering import Vergadering
from tkapi.verslag import Verslag
from tkapi.zaak import Zaak

from .filter import VerwijderdFilter


logger = logging.getLogger(__name__)


class TKApi:
    _verbose = False
    _max_items_per_page = 250
    api_root = 'https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/'

    def __init__(self, api_root=None, verbose=None):
        if api_root is not None:
            TKApi.api_root = api_root
        if verbose is not None:
            TKApi._verbose = verbose

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
    def get_activiteiten(cls, filter, order=None, max_items=None) -> List[Activiteit]:
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

    @classmethod
    def get_verslagen(cls, filter=None, order=None, max_items=None) -> List[Verslag]:
        return cls.get_items(Verslag, filter, order, max_items)

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
        return TKApi.add_filter_to_params(non_deleted_filter, params)

    @classmethod
    def get_all_items(cls, page, max_items=None):
        items = []
        for item in page['value']:
            items.append(item)
            if max_items is not None and len(items) >= max_items:
                return items
        while '@odata.nextLink' in page:
            page = cls._request_json(page['@odata.nextLink'])
            for item in page['value']:
                items.append(item)
                if max_items is not None and len(items) >= max_items:
                    return items
        return items

    @classmethod
    def _request_json(cls, url, params=None, max_items=None):
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
            timeout=60
        )
        if cls._verbose:
            print('url ({} ms): {}'.format(
                int(response.elapsed.total_seconds() * 1000),
                urllib.parse.unquote(response.url))
            )
        if response.status_code in [204, 404]:
            logger.info('HTTP STATUS CODE: {}'.format(response.status_code))
            logger.info('Requested item does not exist: {}'.format(url))
            return {}
        elif response.status_code != 200:
            logger.error('HTTP STATUS CODE: {}'.format(response.status_code))
            logger.error('ODATA ERROR: {}'.format(response.json()['error']['message']))
        return response.json()

    @classmethod
    def get_item(cls, tkitem, id: str):
        url = '{}({})'.format(tkitem.type, id)
        params = tkitem.get_param_expand()
        return tkitem(cls._request_json(url, params))

    @classmethod
    def get_related(cls, tkitem_related, related_url: str, filter=None):
        params = tkitem_related.get_param_expand()
        params = TKApi.add_filter_to_params(filter, params)
        first_page = cls._request_json(related_url, params)
        related_items = []
        if 'value' in first_page:
            items_json = cls.get_all_items(first_page)
            for item_json in items_json:
                related_items.append(tkitem_related(item_json))
        elif first_page:
            related_items.append(tkitem_related(first_page))
        return related_items

    @classmethod
    def get_items(cls, tkitem, filter=None, order=None, max_items=None):
        items = []
        params = cls.create_query_params(tkitem=tkitem, filter=filter, order=order)
        max_items_request = max_items if max_items is not None and max_items <= cls._max_items_per_page else None
        first_page = cls._request_json(tkitem.type, params, max_items=max_items_request)
        items_json = cls.get_all_items(first_page, max_items=max_items)
        for item_json in items_json:
            item = tkitem(item_json)
            items.append(item)
        return items

    @staticmethod
    def create_query_params(tkitem, filter=None, order=None):
        params = tkitem.get_params_default()
        params = TKApi.add_filter_to_params(filter, params)
        params = TKApi.add_non_deleted_filter(params)
        if tkitem.filter_param:
            if params['$filter']:
                params['$filter'] += ' and '
            params['$filter'] += tkitem.filter_param
        if order:
            params['$orderby'] = order.order_by_str
        return params
