import datetime
import requests

import tkapi.util
from tkapi import document

from local_settings import USER, PASSWORD, API_ROOT_URL


class KamerVraag(object):
    def __init__(self, vraag_json):
        # tkapi.util.print_pretty(vraag_json)
        self.vraag_json = vraag_json
        self.document = document.ParlementairDocument(vraag_json)
        if vraag_json['Zaak']:
            self.zaak = vraag_json['Zaak'][0]
        else:
            self.zaak = None
        self.document_url = self.get_document_url()

    def print_info(self):
        print('=============')
        print('document nummer: ' + self.document.nummer)
        print('document titel: ' + self.document.onderwerp)
        print('kamervraag url: ' + self.document_url)
        if self.zaak:
            print('zaak nummer: ' + self.zaak['Nummer'])

    @staticmethod
    def create_from_id(id):
        vraag_json = get_schriftelijke_vraag(id)
        return KamerVraag(vraag_json)

    def get_document_url(self):
        url = ''
        # kamervragen have two url types at officielebekendmakingen, one starting with 'kv-tk' an old ones with 'kv-'
        #TODO: determine date at which this format is switched to reduce the number of requests
        if self.zaak:
            url = 'https://zoek.officielebekendmakingen.nl/kv-tk-' + self.zaak['Nummer']
            response = requests.get(url)
            assert response.status_code == 200
            if 'Errors/404.htm' in response.url:
                url = 'https://zoek.officielebekendmakingen.nl/kv-' + self.zaak['Alias']
                response = requests.get(url)
            if 'Errors/404.htm' in response.url:
                url = ''
        return url


class KamerVragen(object):
    def __init__(self, start_datetime, end_datetime):
        print('KamerVragen::__init__()')
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.vragen = self.create()

    def create(self):
        print('KamerVragen::get_all()')
        vragen = []
        vragen_metadata = get_schriftelijke_vragen(self.start_datetime, self.end_datetime)
        for item in vragen_metadata['value']:
            vragen.append(KamerVraag(item))
        # print_pretty(vragen_metadata)
        while 'odata.nextLink' in vragen_metadata:
            print('KamerVragen::get_all() - next page')
            params = {
                '$format': 'json',
            }
            r = requests.get(API_ROOT_URL + vragen_metadata['odata.nextLink'], params=params, auth=(USER, PASSWORD))
            print(r.url)
            assert r.status_code == 200
            vragen_metadata = r.json()
            for item in vragen_metadata['value']:
                vragen.append(KamerVraag(item))
                print(item['Datum'])
        return vragen


def get_schriftelijke_vragen(start_datetime, end_datetime):
    # TODO: does only get one page of results
    url = 'ParlementairDocument'
    filter_str = "Soort eq 'Schriftelijke vragen'"
    filter_str += ' and '
    filter_str += "Datum gt " + tkapi.util.datetime_to_odata(start_datetime)
    filter_str += ' and '
    filter_str += "Datum lt " + tkapi.util.datetime_to_odata(end_datetime)
    params = {
        '$filter': filter_str,
        '$orderby': 'Datum',
        '$expand': 'Zaak',
        '$format': 'json',
    }
    r = requests.get(API_ROOT_URL + url, params=params, auth=(USER, PASSWORD))
    assert r.status_code == 200
    return r.json()


def get_schriftelijke_vraag(id):
    url = 'ParlementairDocument(guid\'' + id + '\')'
    params = {
        '$expand': 'Zaak',
        '$format': 'json',
    }
    r = requests.get(API_ROOT_URL + url, params=params, auth=(USER, PASSWORD))
    # print(r.url)
    assert r.status_code == 200
    return r.json()


def get_verslag(id):
    url = "Verslag(guid'" + id + "')"
    return get_json(url)


def get_verslag_handeling():
    url = "VerslagHandeling"
    return get_json(url)


def get_parlementaire_documenten():
    url = "ParlementairDocument"
    return get_json(url)


def get_antwoorden():
    url = 'ParlementairDocument'
    params = {
        '$filter': "Soort eq 'Antwoord'",
        '$expand': 'Zaak',
        '$format': 'json',
    }
    r = requests.get(API_ROOT_URL + url, params=params, auth=(USER, PASSWORD))
    assert r.status_code == 200
    return r.json()


def get_json(url):
    params = {
        '$format': 'json',
    }
    r = requests.get(API_ROOT_URL + url, params=params, auth=(USER, PASSWORD))
    print(r.url)
    if r.status_code != 200:
        print(r.text)
    assert r.status_code == 200
    return r.json()
