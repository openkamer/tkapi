import tkapi


class ReisFilter(tkapi.Filter):

    def __init__(self):
        super().__init__()


class Reis(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'PersoonReis'

    @staticmethod
    def create_filter():
        return ReisFilter()

    @property
    def persoon(self):
        from tkapi.persoon import Persoon
        return self.related_item(Persoon)

    @property
    def bestemming(self):
        return self.get_property_or_empty_string('Bestemming')

    @property
    def doel(self):
        return self.get_property_or_empty_string('Doel')

    @property
    def betaald_door(self):
        return self.get_property_or_empty_string('BetaaldDoor')

    @property
    def van(self):
        return self.get_date_or_none('Van')

    @property
    def tot_en_met(self):
        return self.get_date_or_none('TotEnMet')
