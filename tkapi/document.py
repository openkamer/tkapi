import tkapi


class ParlementairDocumentFilter(tkapi.SoortFilter, tkapi.ZaakRelationFilter):

    def filter_date_range(self, start_datetime, end_datetime):
        filter_str = "Datum ge " + tkapi.util.datetime_to_odata(start_datetime)
        self.filters.append(filter_str)
        filter_str = "Datum lt " + tkapi.util.datetime_to_odata(end_datetime)
        self.filters.append(filter_str)

    def filter_empty_agendapunt(self):
        filter_str = 'Agendapunt/any(a: true)'
        self.filters.append(filter_str)

    def filter_onderwerp(self, onderwerp):
        filter_str = 'Onderwerp eq ' + "'" + onderwerp.replace("'", "''") + "'"
        self.filters.append(filter_str)

    def filter_titel(self, titel):
        filter_str = 'Titel eq ' + "'" + titel.replace("'", "''") + "'"
        self.filters.append(filter_str)


class ParlementairDocument(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'ParlementairDocument'
    # expand_param = 'Zaak'
    orderby_param = 'Datum'

    @staticmethod
    def create_filter():
        return ParlementairDocumentFilter()

    @property
    def activiteiten(self):
        from tkapi.activiteit import Activiteit
        return self.related_items(Activiteit)

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def agendapunten(self):
        agendapunten = []
        for zaak in self.zaken:
            agendapunten += zaak.agendapunten
        return agendapunten

    @property
    def dossiers(self):
        if self.kamerstuk:
            return self.kamerstuk.dossiers
        return []

    @property
    def kamerstuk(self):
        from tkapi.kamerstuk import Kamerstuk
        return self.related_item(Kamerstuk)

    @property
    def aanhangselnummer(self):
        return self.get_property_or_empty_string('Aanhangselnummer')

    @property
    def onderwerp(self):
        return self.get_property_or_empty_string('Onderwerp')

    @property
    def datum(self):
        return self.get_date_or_none('Datum')

    @property
    def nummer(self):
        return self.get_property_or_empty_string('Nummer')

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def titel(self):
        return self.get_property_or_empty_string('Titel')

    @property
    def vergaderjaar(self):
        return self.get_property_or_empty_string('Vergaderjaar')

    @property
    def alias(self):
        return self.get_property_or_empty_string('Alias')

    @property
    def dossier_vetnummer(self):
        if self.kamerstuk and self.kamerstuk.dossier and self.kamerstuk.dossier.vetnummer:
            return self.kamerstuk.dossier.vetnummer
        return None
