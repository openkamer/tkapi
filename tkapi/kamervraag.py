import requests

import tkapi
from tkapi import document



class KamerVraag(tkapi.TKItem):
    def __init__(self, vraag_json):
        super().__init__(vraag_json)
        self.document = document.ParlementairDocument(self.json)
        self.document_url = self.get_document_url()

    @property
    def zaak(self):
        if self.json['Zaak']:
            return self.json['Zaak'][0]
        return None

    @property
    def datum(self):
        return self.get_property_or_empty_string('Datum')

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
        else:
            print('no zaak found')
            # tkapi.util.print_pretty(self.json)
        return url


class Antwoord(tkapi.TKItem):
    def __init__(self, antwoord_json):
        super().__init__(antwoord_json)
        self.document = document.ParlementairDocument(self.json)
        self.document_url = self.get_document_url()

    @property
    def zaak(self):
        if self.json['Zaak']:
            return self.json['Zaak'][0]
        return None

    @property
    def datum(self):
        return self.get_property_or_empty_string('Datum')

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
            # tkapi.util.print_pretty(self.document.json)
            url = ''
        return url


def get_kamervragen(start_datetime, end_datetime):
    first_page = get_schriftelijke_vragen_first_page_json(start_datetime, end_datetime)
    items = tkapi.get_all_items(first_page)
    vragen = []
    for item in items:
        vraag = KamerVraag(item)
        vragen.append(vraag)
        print('create vraag for date: ' + str(vraag.datum))
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
    }
    return tkapi.request_json(url, params)


def get_schriftelijke_vraag_json(id):
    url = 'ParlementairDocument(guid\'' + id + '\')'
    params = {
        '$expand': 'Zaak',
    }
    return tkapi.request_json(url, params)


def get_antwoorden(start_datetime, end_datetime):
    first_page = get_antwoorden_first_page_json(start_datetime, end_datetime)
    items = tkapi.get_all_items(first_page)
    antwoorden = []
    for item in items:
        antwoord = Antwoord(item)
        print('create antwoord for date: ' + str(antwoord.datum))
        antwoorden.append(antwoord)
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
    }
    return tkapi.request_json(url, params)
