import tkapi


class Activiteit(tkapi.TKItem):

    def __init__(self, activiteit_json):
        super().__init__(activiteit_json)

    def get_params_default(self):
        return {}

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
    def soort(self):
        return self.get_property_or_empty_string('Nummer')

    # @property
    # def voortouwcommissie(self):
    #     return self.get_property_or_empty_string('Voortouwcommissie')
