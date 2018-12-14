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
