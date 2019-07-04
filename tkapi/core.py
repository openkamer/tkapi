from tkapi.util import util


class TKItem(object):
    url = NotImplementedError
    expand_param = None
    orderby_param = None
    filter_param = ''

    def __init__(self, item_json, *args, **kwargs):
        self.json = item_json

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
        if cls.expand_param:
            params['$expand'] = cls.expand_param
        if cls.orderby_param:
            params['$orderby'] = cls.orderby_param
        elif cls.begin_date_key():
            params['$orderby'] = '{} {}'.format(cls.begin_date_key(), 'desc')
        return params

    @classmethod
    def get_param_expand(cls):
        if not cls.expand_param:
            return {}
        return {
            '$expand': cls.expand_param,
        }

    @property
    def id(self):
        return self.get_property_or_empty_string('Id')

    def print_json(self):
        util.print_pretty(self.json)

    def get_property_or_none(self, property_key):
        if property_key in self.json:
            return self.json[property_key]
        return None

    def get_property_or_empty_string(self, property_key):
        if property_key in self.json and self.json[property_key] is not None:
            return str(self.json[property_key]).strip()
        return ''

    def get_date_from_datetime_or_none(self, property_key):
        if property_key in self.json and self.json[property_key]:
            return util.odatedatetime_to_datetime(self.json[property_key]).date()
        return None

    def get_date_or_none(self, property_key):
        if property_key in self.json and self.json[property_key]:
            return util.odatedate_to_date(self.json[property_key]).date()
        return None

    def get_year_or_none(self, property_key):
        if property_key in self.json and self.json[property_key]:
            return util.odateyear_to_date(self.json[property_key]).date()
        return None

    def get_datetime_or_none(self, property_key):
        if property_key in self.json and self.json[property_key]:
            return util.odatedatetime_to_datetime(self.json[property_key])
        return None

    def get_property_enum_or_none(self, property_key, enum):
        if property_key in self.json and self.json[property_key] is not None:
            return enum(self.json[property_key].strip())
        return None


class TKItemRelated(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items_cache = {}

    @staticmethod
    def create_cache_key(tkitem, filter):
        cache_key = tkitem.__name__
        if filter is not None:
            cache_key += filter.filter_str
        return cache_key

    def set_cache(self, tkitem, filter, items):
        self.items_cache[self.create_cache_key(tkitem, filter)] = items

    def related_items(self, tkitem, filter=None, item_key=None):
        from tkapi.api import Api
        item_key = item_key if item_key is not None else tkitem.url
        navigation_key = item_key + '@odata.navigationLink'
        if navigation_key not in self.json:
            return []
        if item_key in self.json and self.json[item_key] is None:
            return []
        cache_key = self.create_cache_key(tkitem, filter)
        if cache_key in self.items_cache:
            return self.items_cache[cache_key]
        url = self.json[navigation_key]
        items = Api().get_related(tkitem, related_url=url, filter=filter)
        self.set_cache(tkitem, filter, items)
        return items

    def related_items_deep(self, tkitem, filter):
        from tkapi.api import Api
        items = Api().get_related(tkitem, related_url=tkitem.url, filter=filter)
        self.set_cache(tkitem, filter, items)
        return items

    def related_item(self, tkitem, item_key=None):
        related_items = self.related_items(tkitem, item_key=item_key)
        if related_items:
            return related_items[0]
        return None
