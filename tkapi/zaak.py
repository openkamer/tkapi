import tkapi


class Zaak(tkapi.TKItem):
    url = 'Zaak'

    def __init__(self, zaak_json):
        super().__init__(zaak_json)

    @staticmethod
    def get_params_default(start_datetime, end_datetime):
        filter_str = "Datum ge " + tkapi.util.datetime_to_odata(start_datetime)
        filter_str += ' and '
        filter_str += "Datum lt " + tkapi.util.datetime_to_odata(end_datetime)
        params = {
            '$filter': filter_str,
            '$orderby': 'Datum'
        }
        return params

    @staticmethod
    def filter_onderwerp(onderwerp):
        filter_str = "Onderwerp eq " + "'" + onderwerp.replace("'", "''") + "'"
        params = {
            '$filter': filter_str,
        }
        return params

    @property
    def onderwerp(self):
        return self.json['Onderwerp']
