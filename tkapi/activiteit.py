import tkapi


class ActiviteitFilter(tkapi.SoortFilter, tkapi.ZaakRelationFilter):

    def __init__(self):
        super().__init__()


class Activiteit(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Activiteit'
    # expand_param = 'Zaak, ParlementairDocument'

    @property
    def parlementaire_documenten(self):
        from tkapi.document import ParlementairDocument
        return self.related_items(ParlementairDocument)

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def voortouwcommissies(self):
        from tkapi.commissie import VoortouwCommissie
        return self.related_items(VoortouwCommissie)

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
