import tkapi


class Activiteit(tkapi.TKItem):
    url = 'Activiteit'
    expand_param = 'Zaak'

    def __init__(self, activiteit_json):
        super().__init__(activiteit_json)

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
    def zaak(self):
        from tkapi.zaak import Zaak
        return Zaak(self.json['Zaak'])

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
