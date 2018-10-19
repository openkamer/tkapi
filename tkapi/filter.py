class Filter(object):

    def __init__(self):
        super().__init__()
        self.filters = []
        self.filters_or = []

    @property
    def filter_str(self):
        filter_str = ''
        if self.filters:
            sep = ' and '
            filter_str = sep.join(self.filters)
        if self.filters_or:
            if filter_str:
                filter_str += ' and '
            sep = ' or '
            filter_str += sep.join(self.filters_or)
        return filter_str


class SoortFilter(Filter):

    def filter_soort(self, soort, is_or=False):
        filter_str = "Soort eq " + "'" + soort.replace("'", "''") + "'"
        if is_or:
            self.filters_or.append(filter_str)
        else:
            self.filters.append(filter_str)


class VerwijderdFilter(Filter):

    def filter_verwijderd(self, is_deleted=False):
        filter_str = "Verwijderd eq " + str(is_deleted).lower()
        self.filters.append(filter_str)


class ZaakRelationFilter(Filter):

    def filter_empty_zaak(self):
        filter_str = 'Zaak/any(z: true)'
        self.filters.append(filter_str)
