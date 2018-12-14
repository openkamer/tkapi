from .core import TKApiTestCase
from tkapi.zaak import Zaak
from tkapi.order import Order, OrderDirection


class TestOrderQuery(TKApiTestCase):

    def test_order_by_desc(self):
        max_items = 100
        order = Order()
        order.order_by('GestartOp', OrderDirection.DESC)
        zaken = self.api.get_items(Zaak, order=order, max_items=max_items)
        self.assertEqual(max_items, len(zaken))
        zaak_previous = None
        for zaak in zaken:
            if zaak_previous:
                self.assertTrue(zaak.gestart_op <= zaak_previous.gestart_op)
            zaak_previous = zaak

    def test_order_by_asc(self):
        max_items = 100
        order = Order()
        order.order_by('GestartOp', OrderDirection.ASC)
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_begin_date_not_empty()
        zaken = self.api.get_items(Zaak, filter=zaak_filter, order=order, max_items=max_items)
        self.assertEqual(max_items, len(zaken))
        zaak_previous = None
        for zaak in zaken:
            if zaak_previous:
                self.assertTrue(zaak.gestart_op >= zaak_previous.gestart_op)
            zaak_previous = zaak
