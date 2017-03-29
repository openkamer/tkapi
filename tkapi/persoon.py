import tkapi


class Persoon(tkapi.TKItem):
    url = 'Persoon'

    def __init__(self, persoon_json):
        super().__init__(persoon_json)

    @staticmethod
    def get_params_default(require_surname=True):
        params = {
            '$orderby': 'Achternaam',
            '$expand': 'Fractielid, Functie, Afbeelding',
        }
        if require_surname:
            params['$filter'] = "Achternaam ne null",
        return params

    @property
    def achternaam(self):
        return self.get_property_or_empty_string('Achternaam')

    @property
    def initialen(self):
        return self.get_property_or_empty_string('Initialen')

    @property
    def roepnaam(self):
        return self.get_property_or_empty_string('Roepnaam')

    @property
    def voornamen(self):
        return self.get_property_or_empty_string('Voornamen')

    @property
    def geboortedatum(self):
        return self.get_property_or_empty_string('Geboortedatum')

    def __str__(self):
        pretty_print = ''
        if self.roepnaam:
            pretty_print = str(self.roepnaam) + ' '
        pretty_print += str(self.achternaam) + ' '
        if self.initialen:
            pretty_print += '(' + str(self.initialen) + ')'
        return pretty_print
