import requests

import tkapi
from tkapi import api
from tkapi.document import ParlementairDocument


class KamerVraag(ParlementairDocument):

    def __init__(self, vraag_json):
        super().__init__(vraag_json)
        self.document_url = self.get_document_url()

    @staticmethod
    def get_params_default(start_datetime, end_datetime):
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
        return params

    @property
    def zaak(self):
        if self.json['Zaak']:
            assert len(self.json['Zaak']) == 1
            return self.json['Zaak'][0]
        # Try to find a Zaak by Onderwerp, this is needed because Zaak is missing for old Kamervragen.
        # TODO: Remove this ugly workaround if TK fixes this data
        if hasattr(self, 'zaak_found'):
            return self.zaak_found.json
        zaak = api.get_zaak(self.onderwerp)
        if zaak:
            print('WARNING: no Zaak found, trying to find Zaak by onderwerp')
            self.zaak_found = zaak
            return zaak.json
        return None

    @property
    def datum(self):
        return self.get_date_or_none('Datum')

    @property
    def onderwerp(self):
        return self.json['Onderwerp']

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
            # self.print_json()
        return url


class Antwoord(ParlementairDocument):

    def __init__(self, antwoord_json):
        super().__init__(antwoord_json)
        self.document_url = self.get_document_url()

    @staticmethod
    def get_params_default(start_datetime, end_datetime):
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
        return params

    @property
    def zaak(self):
        if self.json['Zaak']:
            return self.json['Zaak'][0]
        return None

    @property
    def datum(self):
        return self.get_date_or_none('Datum')

    def get_document_url(self):
        if not self.vergaderjaar:
            print('document.vergaderjaar is empty, early return')
            return ''
        if not self.aanhangselnummer:
            print('document.aanhangselnummer is empty, early return')
            return ''
        url_id = self.vergaderjaar.replace('-', '') + '-' + self.aanhangselnummer[-4:].lstrip('0')  #20162017-11
        url = 'https://zoek.officielebekendmakingen.nl/ah-tk-' + url_id
        response = requests.get(url)
        assert response.status_code == 200
        if 'Errors/404.htm' in response.url:
            print('WARNING: no antwoord document url found')
            # self.print_json()
            url = ''
        return url
