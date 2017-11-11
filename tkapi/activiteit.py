import tkapi


class ActiviteitFilter(tkapi.SoortFilter, tkapi.ZaakRelationFilter):

    def __init__(self):
        super().__init__()


class Activiteit(tkapi.TKItem):
    url = 'Activiteit'
    expand_param = 'Zaak, Voortouwcommissie/Commissie, ParlementairDocument'

    def __init__(self, activiteit_json):
        super().__init__(activiteit_json)
        self.zaken_cache = []
        self.parlementaire_documenten_cache = []

    @property
    def parlementaire_documenten(self):
        if self.parlementaire_documenten_cache:
            return self.parlementaire_documenten_cache
        from tkapi.document import ParlementairDocument
        parlementaire_documenten = []
        for pd_json in self.json['ParlementairDocument']:
            parlementaire_documenten.append(tkapi.api.get_item(ParlementairDocument, pd_json['Id']))
        self.parlementaire_documenten_cache = parlementaire_documenten
        return parlementaire_documenten

    @staticmethod
    def create_filter():
        return ActiviteitFilter()

    @property
    def begin(self):
        return self.get_date_or_none('Begin')

    @property
    def einde(self):
        return self.get_date_or_none('Einde')

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def nummer(self):
        return self.get_property_or_empty_string('Nummer')

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        if self.zaken_cache:
            return self.zaken_cache
        zaken = []
        for zaak_json in self.json['Zaak']:
            zaken.append(tkapi.api.get_item(Zaak, zaak_json['Id']))
        self.zaken_cache = zaken
        return zaken

    # @property
    # def voortouwcommissie(self):
    #     return self.get_property_or_empty_string('Voortouwcommissie')


## Soorten Activiteiten
# Aanbieding
# Afscheid
# Algemeen overleg
# Beëdiging
# Begrotingsoverleg
# Bijzondere procedure
# Constituerende vergadering
# Delegatievergadering
# E-mailprocedure
# Gesprek
# Hamerstukken
# Herdenking
# Hoorzitting
# Hoorzitting / rondetafelgesprek
# Inbreng feitelijke vragen
# Inbreng schriftelijk overleg
# Inbreng verslag (wetsvoorstel)
# Interpellatiedebat
# Mededelingen
# Notaoverleg
# Ontbijtbijeenkomst Parlement en Wetenschap
# Opening
# Overig
# Petitie
# Plenair debat
# Procedurevergadering
# Regeling van werkzaamheden
# Rondetafelgesprek
# Schriftelijk commentaar algemeen
# Schriftelijk commentaar gericht
# Sluiting
# Stemmingen
# Technische briefing
# Vergadering
# Verklaring
# Vragenuur
# Werkbezoek
# Wetgevingsoverleg
