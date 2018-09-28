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

    # def get_related_id(self, item, key):
    #     item.json


class TKItemRelated(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items_cache = {}

    def set_cache(self, tkitem, items):
        self.items_cache[tkitem.__name__] = items

    def related_items(self, tkitem):
        if tkitem.url + '@odata.navigationLinkUrl' not in self.json:
            return []
        if tkitem.url in self.json and self.json[tkitem.url] is None:
            return []
        if tkitem.__name__ in self.items_cache:
            # print('use cache')
            return self.items_cache[tkitem.__name__]
        items = tkapi.api.get_related(self.__class__, tkitem, self.json['Id'])
        self.set_cache(tkitem, items)
        return items
