import datetime

from tkapi.util import util


class TKItem:
    type = NotImplementedError
    expand_params = None
    orderby_param = None
    filter_param = ''

    def __init__(self, item_json):
        self.json = item_json
        self._items_cache = {}

    def __dict__(self):
        return self.json

    def __getitem__(self, key):
        return self.__dict__()[key]

    def __setitem__(self, key, item):
        self.__dict__()[key] = item

    @staticmethod
    def create_filter():
        raise NotImplementedError

    @staticmethod
    def begin_date_key():
        return 'GewijzigdOp'

    @staticmethod
    def end_date_key():
        return None

    @classmethod
    def get_params_default(cls):
        params = {}
        if cls.expand_params:
            params['$expand'] = ','.join([param for param in cls.expand_params])
        if cls.orderby_param:
            params['$orderby'] = cls.orderby_param
        elif cls.begin_date_key():
            params['$orderby'] = '{} {}'.format(cls.begin_date_key(), 'desc')
        return params

    @classmethod
    def get_param_expand(cls):
        if not cls.expand_params:
            return {}
        params = ','.join([param for param in cls.expand_params])
        return {
            '$expand': params
        }

    @property
    def id(self):
        return self.get_property_or_empty_string('Id')

    @property
    def url(self):
        return self.get_property_or_empty_string('@odata.id')

    @property
    def gewijzigd_op(self):
        return self.get_datetime_or_none('GewijzigdOp')

    def print_json(self):
        util.print_pretty(self.json)

    def get_property_or_none(self, property_key):
        if property_key in self.json:
            return self.json[property_key]
        return None

    def get_property_or_empty_string(self, property_key) -> str:
        if property_key in self.json and self.json[property_key] is not None:
            return str(self.json[property_key]).strip()
        return ''

    def get_date_from_datetime_or_none(self, property_key) -> datetime.date or None:
        if property_key in self.json and self.json[property_key]:
            return util.odatedatetime_to_datetime(self.json[property_key]).date()
        return None

    def get_date_or_none(self, property_key) -> datetime.date or None:
        if property_key in self.json and self.json[property_key]:
            return util.odatedate_to_date(self.json[property_key]).date()
        return None

    def get_year_or_none(self, property_key) -> datetime.date or None:
        if property_key in self.json and self.json[property_key]:
            return util.odateyear_to_date(self.json[property_key]).date()
        return None

    def get_datetime_or_none(self, property_key) -> datetime.datetime or None:
        if property_key in self.json and self.json[property_key]:
            return util.odatedatetime_to_datetime(self.json[property_key])
        return None

    def get_property_enum_or_none(self, property_key, enum):
        if property_key in self.json and self.json[property_key] is not None:
            return enum(self.json[property_key].strip())
        return None

    def get_resource_url_or_none(self):
        resource_key = '#TK.DA.GGM.OData.Resource'
        if resource_key in self.json and self.json[resource_key] is not None:
            return self.json[resource_key]['target']
        return None

    def related_items(self, tkitem, filter=None, item_key=None):
        from tkapi.tkapi import TKApi
        item_key = item_key if item_key is not None else tkitem.type
        navigation_key = '{}{}'.format(item_key, '@odata.navigationLink')
        if navigation_key not in self.json:
            return []
        if item_key in self.json and self.json[item_key] is None:
            return []
        if item_key in self.json:
            if isinstance(self.json[item_key], (list, tuple)):
                items = [tkitem(item_json) for item_json in self.json[item_key] if not item_json.get('Verwijderd', True)]
            else:
                item_json = self.json[tkitem.type]
                items = [tkitem(item_json)] if not item_json.get('Verwijderd', True) else []
            self._set_cache(tkitem, filter, items)
            return items
        cache_key = self._create_cache_key(tkitem, filter)
        if cache_key in self._items_cache:
            return self._items_cache[cache_key]
        url = self.json[navigation_key]
        items = TKApi().get_related(tkitem, related_url=url, filter=filter)
        self._set_cache(tkitem, filter, items)
        return items

    def related_items_deep(self, tkitem, filter):
        from tkapi.tkapi import TKApi
        items = TKApi().get_related(tkitem, related_url=tkitem.type, filter=filter)
        self._set_cache(tkitem, filter, items)
        return items

    def related_item(self, tkitem, item_key=None):
        related_items = self.related_items(tkitem, item_key=item_key)
        if related_items:
            return related_items[0]
        return None

    @staticmethod
    def _create_cache_key(tkitem, filter):
        cache_key = tkitem.__name__
        if filter is not None:
            cache_key += filter.filter_str
        return cache_key

    def _set_cache(self, tkitem, filter, items):
        self._items_cache[self._create_cache_key(tkitem, filter)] = items
