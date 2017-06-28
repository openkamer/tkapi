import tkapi


class Dossier(tkapi.TKItem):
    url = 'Kamerstukdossier'

    def __init__(self, dossier_json):
        super().__init__(dossier_json)

    @staticmethod
    def get_params_default():
        params = {
            '$expand': 'Kamerstuk, Kamerstuk/ParlementairDocument/Zaak',
        }
        return params