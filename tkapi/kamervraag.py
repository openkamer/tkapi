import requests

from tkapi.document import ParlementairDocument
from tkapi.zaak import Zaak


class Kamervraag(ParlementairDocument):
    filter_param = "Soort eq 'Schriftelijke vragen'"
    expand_param = 'Zaak'

    def __init__(self, json):
        super().__init__(json)
        self.document_url = self.get_document_url()

    @staticmethod
    def nearest(zaken, pivot):
        return min(zaken, key=lambda zaak: abs(zaak.gestart_op - pivot))

    @property
    def zaak(self):
        if self.json['Zaak']:
            print('Zaak attribute exists')
            assert len(self.json['Zaak']) == 1
            return self.json['Zaak'][0]
        # Try to find a Zaak by Onderwerp, this is needed because Zaak is missing for old Kamervragen.
        # TODO: Remove this ugly workaround if TK fixes this data
        if hasattr(self, 'zaak_found'):
            return self.zaak_found.json
        print('WARNING: no Zaak found, trying to find Zaak by onderwerp', self.datum, self.onderwerp)
        # self.print_json()
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_onderwerp(self.onderwerp)
        from tkapi.api import Api
        zaken = Api().get_zaken(zaak_filter)
        if len(zaken) == 1:
            print('INFO: zaak found for onderwerp')
            self.zaak_found = zaken[0]
            return zaken[0].json
        elif len(zaken) > 1:
            print('INFO: multiple zaken found for onderwerp: ' + str(self.onderwerp) + ', ' + str(len(zaken)))
            self.zaak_found = Kamervraag.nearest(zaken, self.datum)
            return self.zaak_found
        return None

    @property
    def datum(self):
        return self.get_date_from_datetime_or_none('Datum')

    @property
    def onderwerp(self):
        return self.get_property_or_empty_string('Onderwerp')

    def get_document_url(self):
        url = ''
        # kamervragen have two url types at officielebekendmakingen, one starting with 'kv-tk' an old ones with 'kv-'
        # TODO: determine date at which this format is switched to reduce the number of requests
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
    filter_param = "Soort eq 'Antwoord schriftelijke vragen'"

    def __init__(self, json):
        super().__init__(json)
        self.document_url = self.get_document_url()

    @property
    def datum(self):
        return self.get_date_from_datetime_or_none('Datum')

    def get_document_url(self):
        if not self.vergaderjaar:
            print('document.vergaderjaar is empty, early return')
            return ''
        if not self.aanhangselnummer:
            print('document.aanhangselnummer is empty, early return')
            return ''
        url_id = self.vergaderjaar.replace('-', '') + '-' + self.aanhangselnummer[-4:].lstrip('0')  # 20162017-11
        url = 'https://zoek.officielebekendmakingen.nl/ah-tk-' + url_id
        response = requests.get(url)
        assert response.status_code == 200
        if 'Errors/404.htm' in response.url:
            print('WARNING: no antwoord document url found')
            # self.print_json()
            url = ''
        return url
