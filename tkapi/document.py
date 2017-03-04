import tkapi.util


class ParlementairDocument():
    def __init__(self, document_json):
        # tkapi.util.print_pretty(document_json)
        self.document_json = document_json
        self.onderwerp = document_json['Onderwerp']
        self.datum = document_json['Datum']
        self.id = document_json['Id']
        self.nummer = document_json['Nummer']
        self.soort = document_json['Soort']
        self.titel = document_json['Titel']
