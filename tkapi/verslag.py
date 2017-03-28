import requests

import tkapi.util

import tkapi.document
import tkapi.activiteit


class VerslagAlgemeenOverleg(tkapi.TKItem):
    def __init__(self, document_json):
        super().__init__(document_json)
        self.document = tkapi.document.ParlementairDocument(document_json)
        self.document_url = self.get_document_url()

    @property
    def datum(self):
        return self.get_date_or_none('Datum')

    @property
    def zaak(self):
        if self.json['Zaak']:
            return self.json['Zaak'][0]
        return None

    @property
    def activiteit(self):
        if self.json['Activiteit']:
            return tkapi.activiteit.Activiteit(self.json['Activiteit'][0])
        return None

    @property
    def kamerstuk(self):
        return self.get_property_or_empty_string('Kamerstuk')

    @property
    def dossier(self):
        return self.get_property_or_empty_string('Kamerstukdossier')

    def get_document_url(self):
        url = ''
        if self.dossier and self.kamerstuk:
            kamerstuk_id = str(self.dossier['Vetnummer'])
            if self.dossier['Toevoeging'] and '(' not in self.dossier['Toevoeging']:
                kamerstuk_id += '-' + str(self.dossier['Toevoeging'])
            kamerstuk_id += '-' + str(self.kamerstuk['Ondernummer'])
            url = 'https://zoek.officielebekendmakingen.nl/kst-' + kamerstuk_id
            response = requests.get(url)
            assert response.status_code == 200
            if 'Errors/404.htm' in response.url:
                print('WARNING: no verslag document url found')
                # tkapi.util.print_pretty(self.document.json)
                url = ''
        else:
            print('no dossier or kamerstuk found')
            # tkapi.util.print_pretty(self.json)
        return url


def get_verslagen_van_algemeen_overleg(start_datetime, end_datetime):
    verslagen = []
    first_page = get_verslag_algemeen_overleg_first_page_json(start_datetime, end_datetime)
    items = tkapi.get_all_items(first_page)
    for item in items:
        verslag = VerslagAlgemeenOverleg(item)
        verslagen.append(verslag)
        print(verslag.datum)
    return verslagen


def get_verslag_algemeen_overleg_first_page_json(start_datetime, end_datetime):
    url = 'ParlementairDocument'
    filter_str = "Soort eq 'Verslag van een algemeen overleg'"
    filter_str += ' and '
    filter_str += "Datum ge " + tkapi.util.datetime_to_odata(start_datetime)
    filter_str += ' and '
    filter_str += "Datum lt " + tkapi.util.datetime_to_odata(end_datetime)
    params = {
        '$filter': filter_str,
        '$orderby': 'Datum',
        '$expand': 'Zaak, Activiteit/Voortouwcommissie, Kamerstuk/Kamerstukdossier',  # Activiteit/Vergadering, Activiteit/Voortouwcommissie/Commissie
    }
    return tkapi.request_json(url, params)