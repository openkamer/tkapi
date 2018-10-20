from enum import Enum
import requests

import tkapi
from tkapi.document import ParlementairDocument


class VerslagSoort(Enum):
    EINDPUBLICATIE = 'Eindpublicatie'
    TUSSENPUBLICATIE = 'Tussenpublicatie'
    VOORPUBLICATIE = 'Voorpublicatie'


class VerslagFilter(tkapi.SoortFilter):

    def __init__(self):
        super().__init__()


class Verslag(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Verslag'

    @staticmethod
    def create_filter():
        return VerslagFilter()

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def vergadering(self):
        from tkapi.vergadering import Vergadering
        return self.related_item(Vergadering)

    @property
    def status(self):
        return self.get_property_or_empty_string('Status')


class VerslagAlgemeenOverleg(ParlementairDocument):
    filter_param = "Soort eq 'Verslag van een algemeen overleg'"
    # expand_param = 'Zaak/Voortouwcommissie/Commissie, Activiteit/Voortouwcommissie/Commissie, Activiteit/Volgcommissie/Commissie, Kamerstuk/Kamerstukdossier'

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
    def document_url(self):
        url = ''
        if self.dossiers:
            dossier = self.dossiers[0]
            kamerstuk_id = str(dossier.vetnummer)
            if dossier.toevoeging and '(' not in dossier.toevoeging:
                kamerstuk_id += '-' + str(dossier.toevoeging)
            kamerstuk_id += '-' + str(self.kamerstuk.ondernummer)
            url = 'https://zoek.officielebekendmakingen.nl/kst-' + kamerstuk_id
            response = requests.get(url)
            assert response.status_code == 200
            if 'Errors/404.htm' in response.url:
                print('WARNING: no verslag document url found')
                url = ''
        else:
            print('no dossier or kamerstuk found')
        return url
