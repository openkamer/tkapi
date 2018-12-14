from enum import Enum


class OrderDirection(Enum):
    ASC = 'asc'
    DESC = 'desc'


class Order(object):

    def __init__(self):
        super().__init__()
        self.order_by_str = None

    def order_by(self, property, type=OrderDirection.ASC):
        """
        :param property: the property to order by
        :param type: asc or desc
        :return: the OData orderby parameter
        """
        self.order_by_str = '{} {}'.format(str(property), type.value)

    def order_by_begin_date(self, tkitemclass, type=OrderDirection.ASC):
        """
        :param tkitemclass: the TKItem class
        :param type: asc or desc
        :return: the OData orderby parameter
        """
        if tkitemclass.begin_date_key() is None:
            return ''
        self.order_by_str = '{} {}'.format(tkitemclass.begin_date_key(), type.value)
