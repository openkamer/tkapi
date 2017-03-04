import tkapi.util


class ParlementairDocument():
    def __init__(self, document_json):
        # tkapi.util.print_pretty(document_json)
        self.document_json = document_json
        self.aanhangselnummer = document_json['Aanhangselnummer']
        self.onderwerp = document_json['Onderwerp']
        self.datum = document_json['Datum']
        self.id = document_json['Id']
        self.nummer = document_json['Nummer']
        self.soort = document_json['Soort']
        self.titel = document_json['Titel']
        self.vergaderjaar = document_json['Vergaderjaar']


def get_parlementaire_documenten():
    url = "ParlementairDocument"
    return tkapi.util.get_json(url)
