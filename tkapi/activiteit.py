import tkapi.util


class Activiteit():
    def __init__(self, activiteit_json):
        self.begin = tkapi.util.odatedatetime_to_datetime(activiteit_json['Begin'])
        self.end = tkapi.util.odatedatetime_to_datetime(activiteit_json['Einde'])
        self.soort = activiteit_json['Soort']
        self.nummer = activiteit_json['Nummer']