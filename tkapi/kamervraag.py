import requests

from tkapi.document import Document
from tkapi.zaak import ZaakSoort


class Kamervraag(Document):
    filter_param = "Soort eq '{}'".format(ZaakSoort.SCHRIFTELIJKE_VRAGEN.value)

    def __init__(self, json):
        super().__init__(json)

    @staticmethod
    def nearest(zaken, pivot):
        return min(zaken, key=lambda zaak: abs(zaak.gestart_op - pivot))

    @property
    def datum(self):
        return self.get_date_from_datetime_or_none('Datum')

    @property
    def onderwerp(self):
        return self.get_property_or_empty_string('Onderwerp')

    @property
    def document_url(self):
        print('get officielebekendmakingen.nl document url')
        url = ''
        # kamervragen have two url types at officielebekendmakingen, one starting with 'kv-tk' an old ones with 'kv-'
        # TODO: determine date at which this format is switched to reduce the number of requests
        for zaak in self.zaken:
            url = 'https://zoek.officielebekendmakingen.nl/kv-tk-' + zaak.nummer
            response = requests.get(url, timeout=60)
            if response.status_code != 200:
                print('ERROR {} getting url {}'.format(response.status_code, url))
            if response.status_code == 404 or 'Errors/404.htm' in response.url and zaak.alias:
                url = 'https://zoek.officielebekendmakingen.nl/kv-' + zaak.alias
                response = requests.get(url, timeout=60)
            if response.status_code == 404 or 'Errors/404.htm' in response.url:
                url = ''
        if not url:
            print('no zaak found')
            # self.print_json()
        print('url found:', url)
        return url


class Antwoord(Document):
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
        response = requests.get(url, timeout=60)
        assert response.status_code == 200
        if 'Errors/404.htm' in response.url:
            print('WARNING: no antwoord document url found')
            # self.print_json()
            url = ''
        return url
