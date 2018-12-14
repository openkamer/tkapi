from .core import TKApiTestCase
from tkapi.zaak import Zaak
from tkapi.order import Order, OrderDirection


class TestOrderQuery(TKApiTestCase):

    def test_order_by_desc(self):
        max_items = 100
        order_direction = OrderDirection.DESC
        self.check_order_by(filter=None, max_items=max_items, order_direction=order_direction)

    def test_order_by_asc(self):
        max_items = 100
        order_direction = OrderDirection.ASC
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_begin_date_not_empty()
        self.check_order_by(filter=zaak_filter, max_items=max_items, order_direction=order_direction)

    def test_order_by_date_asc(self):
        max_items = 100
        order_direction = OrderDirection.ASC
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_begin_date_not_empty()
        self.check_order_by(filter=zaak_filter, max_items=max_items, order_direction=order_direction)

    def check_order_by(self, filter, max_items, order_direction=OrderDirection.ASC):
        order = Order()
        order.order_by_begin_date(Zaak, order_direction)
        zaken = self.api.get_items(Zaak, filter=filter, order=order, max_items=max_items)
        self.assertEqual(max_items, len(zaken))
        zaak_previous = None
        for zaak in zaken:
            if zaak_previous:
                if order_direction == OrderDirection.ASC:
                    self.assertTrue(zaak.gestart_op >= zaak_previous.gestart_op)
                elif order_direction == OrderDirection.DESC:
                    self.assertTrue(zaak.gestart_op <= zaak_previous.gestart_op)
                else:
                    self.fail('order direction not properly defined')
            zaak_previous = zaak
