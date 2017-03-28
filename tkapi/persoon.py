import tkapi


class Persoon(tkapi.TKItem):
    def __init__(self, persoon_json):
        super().__init__(persoon_json)

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


def get_personen(require_surname=True, max_items=None):
    personen = []
    page = get_personen_first_page_json(require_surname)
    commissie_items = tkapi.get_all_items(page, max_items=max_items)
    for item in commissie_items:
        personen.append(Persoon(item))
    return personen


def get_personen_first_page_json(require_surname=True):
    url = 'Persoon'
    params = {
        '$orderby': 'Achternaam',
        '$expand': 'Fractielid, Functie, Afbeelding',
    }
    if require_surname:
        params['$filter'] = "Achternaam ne null",
    return tkapi.request_json(url, params)
