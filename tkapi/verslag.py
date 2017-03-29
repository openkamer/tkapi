import requests

import tkapi.util

from tkapi.document import ParlementairDocument
import tkapi.activiteit


class VerslagAlgemeenOverleg(ParlementairDocument):
    url = 'ParlementairDocument'

    def __init__(self, document_json):
        super().__init__(document_json)
        self.document_url = self.get_document_url()

    @staticmethod
    def get_params_default(start_datetime, end_datetime):
        filter_str = "Soort eq 'Verslag van een algemeen overleg'"
        filter_str += ' and '
        filter_str += "Datum ge " + tkapi.util.datetime_to_odata(start_datetime)
        filter_str += ' and '
        filter_str += "Datum lt " + tkapi.util.datetime_to_odata(end_datetime)
        params = {
            '$filter': filter_str,
            '$orderby': 'Datum',
            '$expand': 'Zaak/Voortouwcommissie/Commissie, Activiteit/Voortouwcommissie/Commissie, Activiteit/Volgcommissie/Commissie, Kamerstuk/Kamerstukdossier',  # Activiteit/Vergadering, Activiteit/Voortouwcommissie/Commissie
        }
        return params

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

    # @property
    # def commissie(self):
    #     if self.zaak and self.zaak['Voortouwcommissie']:
    #         for commissie in self.zaak['Voortouwcommissie']:
    #             print(commissie['Commissie'])
    #         return self.zaak['Voortouwcommissie'][0]['Commissie']
    #     return None
    #
    # @property
    # def volgcommissie(self):
    #     if self.activiteit and self.activiteit['Volgcommissie']:
    #         return self.activiteit['Volgcommissie'][0]['Commissie']
    #     return None

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
                # self.print_json()
                url = ''
        else:
            print('no dossier or kamerstuk found')
            # self.print_json()
        return url
