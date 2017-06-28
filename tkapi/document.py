import tkapi


class ParlementairDocument(tkapi.TKItem):
    url = 'ParlementairDocument'

    def __init__(self, document_json):
        super().__init__(document_json)
        # tkapi.util.print_pretty(document_json)

    @staticmethod
    def get_params_default(start_datetime, end_datetime):
        filter_str = "Datum ge " + tkapi.util.datetime_to_odata(start_datetime)
        filter_str += ' and '
        filter_str += "Datum lt " + tkapi.util.datetime_to_odata(end_datetime)
        params = {
            '$filter': filter_str,
            '$orderby': 'Datum',
            '$expand': 'Zaak',
        }
        return params

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
    def title(self):
        return self.get_property_or_empty_string('Titel')

    @property
    def vergaderjaar(self):
        return self.get_property_or_empty_string('Vergaderjaar')


""" mogelijk soorten


"""