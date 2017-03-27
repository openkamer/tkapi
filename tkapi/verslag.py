import requests

import tkapi.util

import tkapi.document
import tkapi.activiteit

from local_settings import USER, PASSWORD, API_ROOT_URL


class VerslagAlgemeenOverleg(object):
    def __init__(self, metadata):
        self.metadata = metadata
        self.document = tkapi.document.ParlementairDocument(metadata)
        self.zaak = None
        self.activiteit = None
        self.kamerstuk = None
        self.dossier = None
        if metadata['Zaak']:
            self.zaak = metadata['Zaak'][0]
        if metadata['Activiteit']:
            self.activiteit = tkapi.activiteit.Activiteit(metadata['Activiteit'][0])
        else:
            print('Geen activiteit gevonden!')
        if metadata['Kamerstuk']:
            self.kamerstuk = metadata['Kamerstuk']
            if self.kamerstuk['Kamerstukdossier']:
                self.dossier = self.kamerstuk['Kamerstukdossier']
        self.document_url = self.get_document_url()

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
                tkapi.util.print_pretty(self.document.document_json)
                url = ''
        else:
            print('no dossier or kamerstuk found in metadata')
            tkapi.util.print_pretty(self.metadata)
        return url


def get_verslagen_van_algemeen_overleg(start_datetime, end_datetime):
    verslagen = []
    verslagen_metadata = get_verslag_algemeen_overleg_first_page_json(start_datetime, end_datetime)
    for item in verslagen_metadata['value']:
        verslagen.append(VerslagAlgemeenOverleg(item))
        print(item['Datum'])
    while 'odata.nextLink' in verslagen_metadata:
        params = {
            '$format': 'json',
        }
        r = requests.get(API_ROOT_URL + verslagen_metadata['odata.nextLink'], params=params, auth=(USER, PASSWORD))
        assert r.status_code == 200
        verslagen_metadata = r.json()
        for item in verslagen_metadata['value']:
            verslagen.append(VerslagAlgemeenOverleg(item))
            print(item['Datum'])
    return verslagen


def get_verslag_algemeen_overleg_first_page_json(start_datetime, end_datetime):
    # TODO: does only get one page of results
    url = 'ParlementairDocument'
    filter_str = "Soort eq 'Verslag van een algemeen overleg'"
    filter_str += ' and '
    filter_str += "Datum ge " + tkapi.util.datetime_to_odata(start_datetime)
    filter_str += ' and '
    filter_str += "Datum lt " + tkapi.util.datetime_to_odata(end_datetime)
    params = {
        '$filter': filter_str,
        '$orderby': 'Datum',
        '$expand': 'Zaak, Activiteit, Kamerstuk/Kamerstukdossier',  # Activiteit/Vergadering, Activiteit/Voortouwcommissie/Commissie
        '$format': 'json',
    }
    r = requests.get(API_ROOT_URL + url, params=params, auth=(USER, PASSWORD))
    assert r.status_code == 200
    return r.json()