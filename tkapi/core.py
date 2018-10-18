import tkapi.util


class TKItem(object):
    url = ''
    expand_param = ''
    orderby_param = ''
    filter_param = ''

    @staticmethod
    def create_filter():
        return NotImplementedError

    def __init__(self, item_json, *args, **kwargs):
        self.json = item_json

    def __dict__(self):
        return self.json

    def __getitem__(self, key):
        return self.__dict__()[key]

    def __setitem__(self, key, item):
        self.__dict__()[key] = item

    @classmethod
    def get_params_default(cls):
        return {
            '$expand': cls.expand_param,
            '$orderby': cls.orderby_param,
        }

    @classmethod
    def get_param_expand(cls):
        return {
            '$expand': cls.expand_param,
        }

    @property
    def id(self):
        return self.get_property_or_empty_string('Id')

    def print_json(self):
        tkapi.util.print_pretty(self.json)

    def get_property_or_none(self, property_key):
        if property_key in self.json and self.json[property_key]:
            return self.json[property_key]
        return None

    def get_property_or_empty_string(self, property_key):
        if property_key in self.json and self.json[property_key]:
            return str(self.json[property_key])
        return ''

    def get_date_or_none(self, property_key):
        if property_key in self.json and self.json[property_key]:
            return tkapi.util.odatedatetime_to_datetime(self.json[property_key]).date()
        return None

    def get_datetime_or_none(self, property_key):
        if property_key in self.json and self.json[property_key]:
            return tkapi.util.odatedatetime_to_datetime(self.json[property_key])
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

    def related_items(self, tkitem, filter=None):
        from tkapi.api import Api
        if tkitem.url + '@odata.navigationLinkUrl' not in self.json:
            return []
        if tkitem.url in self.json and self.json[tkitem.url] is None:
            return []
        cache_key = self.create_cache_key(tkitem, filter)
        if cache_key in self.items_cache:
            return self.items_cache[cache_key]
        url = self.json[tkitem.url + '@odata.navigationLinkUrl']
        # print(url)
        items = Api().get_related(tkitem, related_url=url, filter=filter)
        self.set_cache(tkitem, filter, items)
        return items

    def related_item(self, tkitem):
        related_items = self.related_items(tkitem)
        if related_items:
            return related_items[0]
        return None
