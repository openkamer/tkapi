import tkapi


class Actor(tkapi.TKItemRelated, tkapi.TKItem):
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


class ZaakActor(Actor):
    url = 'ZaakActor'

    @property
    def relatie(self):
        return self.get_property_or_empty_string('Relatie')

    @property
    def naam(self):
        return self.get_property_or_empty_string('ActorNaam')

    @property
    def is_voortouwcommissie(self):
        return self.relatie == 'Voortouwcommissie'

    @property
    def voortouwcommissie(self):
        if self.is_voortouwcommissie:
            return self.commissie
