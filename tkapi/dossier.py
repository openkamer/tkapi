import tkapi


class DossierFilter(tkapi.Filter):

    def filter_vetnummer(self, vetnummer):
        filter_str = "Vetnummer eq " + str(vetnummer)
        self.filters.append(filter_str)

    def filter_zaak(self, zaak_number):
        filter_str = 'Kamerstuk/any(ks:ks/ParlementairDocument/Zaak/any(z:z/Nummer eq ' \
                     + "'" + str(zaak_number) + "'" + '))'
        self.filters.append(filter_str)

    def filter_afgesloten(self, is_afgesloten):
        is_afgesloten_str = 'true' if is_afgesloten else 'false'
        filter_str = "Afgesloten eq " + is_afgesloten_str
        self.filters.append(filter_str)

    def filter_zaken(self, zaak_numbers):
        filter_str = 'Kamerstuk/any(ks:ks/ParlementairDocument/Zaak/any(z:'
        zaak_nummer_strs = []
        for nummer in zaak_numbers:
            zaak_nummer_strs.append('(z/Nummer eq ' + "'" + str(nummer) + "')")
        filter_str += ' or '.join(zaak_nummer_strs)
        filter_str += '))'
        self.filters.append(filter_str)


class Dossier(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Kamerstukdossier'
    expand_param = ''

    @staticmethod
    def create_filter():
        return DossierFilter()

    @property
    def kamerstukken(self):
        from tkapi.kamerstuk import Kamerstuk
        return self.related_items(Kamerstuk)

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def parlementaire_documenten(self):
        return [kamerstuk.parlementair_document for kamerstuk in self.kamerstukken]

    @property
    def vetnummer(self):
        return self.get_property_or_none('Vetnummer')

    @property
    def toevoeging(self):
        return self.get_property_or_none('Toevoeging')

    @property
    def afgesloten(self):
        return self.json['Afgesloten']

    @property
    def titel(self):
        return self.get_property_or_empty_string('Titel')

    @property
    def organisatie(self):
        return self.get_property_or_empty_string('Organisatie')
