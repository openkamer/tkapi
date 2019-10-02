
# taken from: https://opendata.tweedekamer.nl/documentatie/Document
DOCUMENT_TYPES = '''
Aanbiedingsbrief, Aanhangsel van de Handelingen, Advies aan Presidium, Advies Afdeling advisering Raad van State, Advies Afdeling advisering Raad van State en Nader rapport, Advies Afdeling advisering Raad van State en Reactie van de initiatiefnemer(s), Advies commissie, Advies van andere adviesorganen, Adviesaanvraag Afdeling advisering Raad van State, Agenda plenaire vergadering, Agenda procedurevergadering, Amendement, Antwoord schriftelijke vragen, Antwoord schriftelijke vragen (nader), Begrotingstoelichting, Besluitenlijst procedurevergadering, Bijgewerkte tekst, Bijlage, Brief Afdeling advisering Raad van State, Brief Algemene Rekenkamer, Brief commissie, Brief commissie aan bewindspersoon, Brief CTIVD, Brief Eerste Kamer, Brief Europese Commissie, Brief formateur, Brief informateur, Brief Kamer, Brief lid / fractie, Brief Nationale ombudsman, Brief president Hoge Raad, Brief Presidium, Brief regering, Brief verkenner, Convocatie commissieactiviteit, Convocatie inbreng, Eindtekst, EU-voorstel, Geleidende brief, Groenboek/witboek, Inbreng verslag schriftelijk overleg, Initiatiefnota, Interpellatievragen, Jaarverslag, Koninklijke boodschap, Lijst met EU-voorstellen, Lijst van ingekomen stukken, Lijst van vragen, Lijst van vragen en antwoorden, Mededeling, Mededeling (uitstel antwoord), Memorie van toelichting, Memorie van toelichting (initiatiefvoorstel), Mondelinge vragen, Motie, Motie (gewijzigd/nader), Nader rapport, Nota, Nota n.a.v. het (nader/tweede nader/enz.) verslag, Nota van verbetering, Nota van wijziging, Nota van wijziging (initiatiefvoorstel), Onderzoeksvoorstel, Oorspronkelijke tekst, Overig, Position paper, Raming van de uitgaven, Rapport, Rapport Algemene Rekenkamer, Reactie initiatiefnemer(s), Schriftelijke vragen, Sprekerslijst, Stemmingslijst, Stemmingsuitslagen, Stenogram, Verslag (initiatief)wetsvoorstel (nader), Verslag commissie Verzoekschriften en de Burgerinitiatieven, Verslag houdende een lijst van vragen en antwoorden, Verslag van een algemeen overleg, Verslag van een bijeenkomst, Verslag van een hoorzitting / rondetafelgesprek, Verslag van een notaoverleg, Verslag van een politieke dialoog, Verslag van een rapporteur, Verslag van een schriftelijk overleg, Verslag van een werkbezoek, Verslag van een wetgevingsoverleg, Voordracht, Voorlichting Afdeling advisering Raad van State, Voorstel tot wijziging Reglement van Orde, Voorstel van wet, Voorstel van wet (initiatiefvoorstel), Voorstel van wet (tweede lezing), Wetenschappelijke factsheet, Wijzigingen voorgesteld door de regering
'''


def main():
    document_types = DOCUMENT_TYPES.split(',')
    for doc_type in document_types:
        doc_type = doc_type.strip()
        doc_type_capitals = doc_type.upper()
        doc_type_capitals = doc_type_capitals.replace(' ', '_')
        doc_type_capitals = doc_type_capitals.replace('/', '')
        doc_type_capitals = doc_type_capitals.replace('-', '_')
        doc_type_capitals = doc_type_capitals.replace('.', '')
        doc_type_capitals = doc_type_capitals.replace('(', '')
        doc_type_capitals = doc_type_capitals.replace(')', '')
        print("{} = '{}'".format(doc_type_capitals, doc_type))


if '__main__' == __name__:
    main()
