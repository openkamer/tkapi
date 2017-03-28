import tkapi
from tkapi.persoon import Persoon


class Commissie(tkapi.TKItem):
    def __init__(self, commissie_json):
        super().__init__(commissie_json)
        self.leden = []
        for lid in self.json['Lid']:
            self.leden.append(CommissieLid(lid))

    @property
    def afkorting(self):
        return self.get_property_or_empty_string('Afkorting')

    @property
    def naam(self):
        return self.get_property_or_empty_string('NaamNL')

    @property
    def naam_web(self):
        return self.get_property_or_empty_string('NaamWebNL')

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    def __str__(self):
        pretty_print = self.id + ': '
        pretty_print += self.naam
        if self.afkorting:
            pretty_print += ' (' + self.afkorting + ')'
        return pretty_print


class CommissieLid(tkapi.TKItem):
    def __init__(self, lid_json):
        super().__init__(lid_json)

    @property
    def vast_van(self):
        if self.json['VastVan']:
            return tkapi.util.odatedatetime_to_datetime(self.json['VastVan']).date()
        return None

    @property
    def vast_tot_en_met(self):
        if self.json['VastTotEnMet']:
            return tkapi.util.odatedatetime_to_datetime(self.json['VastVan']).date()
        return None

    @property
    def persoon(self):
        if self.json['VastPersoon']:
            return Persoon(self.json['VastPersoon'])
        return None

    def __str__(self):
        pretty_print = ''
        if self.persoon:
            pretty_print = str(self.persoon)
        if self.vast_van:
            pretty_print += ': ' + str(self.vast_van)
        if self.vast_tot_en_met:
            pretty_print += ' - ' + str(self.vast_tot_en_met)
        return pretty_print


def get_commissies(max_items=None):
    commissies = []
    page = get_commissies_first_page_json()
    commissie_items = tkapi.get_all_items(page, max_items=max_items)
    for item in commissie_items:
        commissies.append(Commissie(item))
    return commissies


def get_commissies_first_page_json():
    url = 'Commissie'
    params = {
        # '$filter': filter_str,
        # '$orderby': 'Datum',
        '$expand': 'Organisatie, Lid/VastPersoon',
    }
    return tkapi.request_json(url, params)
