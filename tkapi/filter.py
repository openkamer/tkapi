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

    def filter_soort(self, soort):
        filter_str = "Soort eq " + "'" + soort.replace("'", "''") + "'"
        self.filters.append(filter_str)
