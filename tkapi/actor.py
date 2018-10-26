import tkapi


class Actor(tkapi.TKItemRelated, tkapi.TKItem):
    url = NotImplementedError

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def parlementaire_documenten(self):
        from tkapi.document import ParlementairDocument
        return self.related_items(ParlementairDocument)

    @property
    def stemming(self):
        from tkapi.stemming import Stemming
        return self.related_item(Stemming)
