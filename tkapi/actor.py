import tkapi


class Actor(tkapi.TKItem):
    url = NotImplementedError

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def documenten(self):
        from tkapi.document import Document
        return self.related_items(Document)

    @property
    def stemming(self):
        from tkapi.stemming import Stemming
        return self.related_item(Stemming)

    @property
    def commissie(self):
        from tkapi.commissie import Commissie
        return self.related_item(Commissie)
