import datetime
import requests

import tkapi.util
from tkapi import document

from local_settings import USER, PASSWORD, API_ROOT_URL


class KamerVraag(object):
    def __init__(self, vraag_json):
        self.vraag_json = vraag_json
        self.document = document.ParlementairDocument(vraag_json)
        if vraag_json['Zaak']:
            self.zaak = vraag_json['Zaak'][0]
        else:
            self.zaak = None
        self.document_url = self.get_document_url()

    @staticmethod
    def create_from_id(id):
        vraag_json = get_schriftelijke_vraag_json(id)
        return KamerVraag(vraag_json)

    def get_document_url(self):
        url = ''
        # kamervragen have two url types at officielebekendmakingen, one starting with 'kv-tk' an old ones with 'kv-'
        #TODO: determine date at which this format is switched to reduce the number of requests
        if self.zaak:
            url = 'https://zoek.officielebekendmakingen.nl/kv-tk-' + self.zaak['Nummer']
            response = requests.get(url)
            assert response.status_code == 200
            if 'Errors/404.htm' in response.url and 'Alias' in self.zaak and self.zaak['Alias']:
                url = 'https://zoek.officielebekendmakingen.nl/kv-' + self.zaak['Alias']
                response = requests.get(url)
            if 'Errors/404.htm' in response.url:
                url = ''
        return url


class Antwoord(object):
    def __init__(self, antwoord_json):
        self.antwoord_json = antwoord_json
        self.document = document.ParlementairDocument(antwoord_json)
        if antwoord_json['Zaak']:
            self.zaak = antwoord_json['Zaak'][0]
        else:
            self.zaak = None
        self.document_url = self.get_document_url()

    def get_document_url(self):
        if not self.document.vergaderjaar:
            print('document.vergaderjaar is empty, early return')
            return ''
        if not self.document.aanhangselnummer:
            print('document.aanhangselnummer is empty, early return')
            return ''
        url_id = self.document.vergaderjaar.replace('-', '') + '-' + self.document.aanhangselnummer[-4:].lstrip('0')  #20162017-11
        url = 'https://zoek.officielebekendmakingen.nl/ah-tk-' + url_id
        response = requests.get(url)
        assert response.status_code == 200
        if 'Errors/404.htm' in response.url:
            print('WARNING: no antwoord document url found')
            tkapi.util.print_pretty(self.document.document_json)
            url = ''
        return url


def get_kamervragen(start_datetime, end_datetime):
    vragen = []
    vragen_metadata = get_schriftelijke_vragen_first_page_json(start_datetime, end_datetime)
    for item in vragen_metadata['value']:
        vragen.append(KamerVraag(item))
        print(item['Datum'])
    while 'odata.nextLink' in vragen_metadata:
        params = {
            '$format': 'json',
        }
        r = requests.get(API_ROOT_URL + vragen_metadata['odata.nextLink'], params=params, auth=(USER, PASSWORD))
        assert r.status_code == 200
        vragen_metadata = r.json()
        for item in vragen_metadata['value']:
            vragen.append(KamerVraag(item))
            print(item['Datum'])
    return vragen


def get_schriftelijke_vragen_first_page_json(start_datetime, end_datetime):
    # TODO: does only get one page of results
    url = 'ParlementairDocument'
    filter_str = "Soort eq 'Schriftelijke vragen'"
    filter_str += ' and '
    filter_str += "Datum ge " + tkapi.util.datetime_to_odata(start_datetime)
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


def get_schriftelijke_vraag_json(id):
    url = 'ParlementairDocument(guid\'' + id + '\')'
    params = {
        '$expand': 'Zaak',
        '$format': 'json',
    }
    r = requests.get(API_ROOT_URL + url, params=params, auth=(USER, PASSWORD))
    # print(r.url)
    assert r.status_code == 200
    return r.json()


def get_antwoorden(start_datetime, end_datetime):
    antwoorden = []
    antwoorden_json = get_antwoorden_first_page_json(start_datetime, end_datetime)
    for item in antwoorden_json["value"]:
        antwoorden.append(Antwoord(item))
        print(item['Datum'])
    while 'odata.nextLink' in antwoorden_json:
        params = {
            '$format': 'json',
        }
        r = requests.get(API_ROOT_URL + antwoorden_json['odata.nextLink'], params=params, auth=(USER, PASSWORD))
        assert r.status_code == 200
        antwoorden_json = r.json()
        for item in antwoorden_json['value']:
            antwoorden.append(Antwoord(item))
            print(item['Datum'])
    return antwoorden


def get_antwoorden_first_page_json(start_datetime, end_datetime):
    url = 'ParlementairDocument'
    filter_str = "Soort eq 'Antwoord'"
    filter_str += ' and '
    filter_str += "Datum ge " + tkapi.util.datetime_to_odata(start_datetime)
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
