from enum import Enum


class Filter(object):

    def __init__(self):
        super().__init__()
        self._filters = []
        self._filters_or = []

    def add_filter_str(self, filter_str, is_or=False):
        if is_or:
            self._filters_or.append(filter_str)
        else:
            self._filters.append(filter_str)

    @property
    def filter_str(self):
        filter_str = ''
        if self._filters:
            sep = ' and '
            filter_str = sep.join(self._filters)
        if self._filters_or:
            if filter_str:
                filter_str += ' and '
            sep = ' or '
            filter_str += sep.join(self._filters_or)
        return filter_str


class SoortFilter(Filter):

    def filter_soort(self, soort, is_or=False):
        if isinstance(soort, Enum):
            soort = soort.value
        filter_str = "Soort eq " + "'" + soort.replace("'", "''") + "'"
        self.add_filter_str(filter_str, is_or)


class VerwijderdFilter(Filter):

    def filter_verwijderd(self, is_deleted=False):
        filter_str = "Verwijderd eq " + str(is_deleted).lower()
        self._filters.append(filter_str)


class RelationsFilter(Filter):

    @property
    def related_url(self):
        raise NotImplementedError

    def filter_non_empty(self, related_entity):
        filter_str = '{}/any(z:z ne null)'.format(related_entity.url)
        self._filters.append(filter_str)

    # TODO BR: should this not be the public function
    def _filter_non_empty(self):
        filter_str = self.related_url + '/any(z:z ne null)'
        self._filters.append(filter_str)

    def _filter_empty(self):
        filter_str = self.related_url + '/any(z:z eq null)'
        self._filters.append(filter_str)


class RelationFilter(Filter):

    @property
    def related_url(self):
        raise NotImplementedError

    def filter_non_empty(self):
        filter_str = self.related_url + ' ne null'
        self._filters.append(filter_str)

    def filter_empty(self):
        filter_str = self.related_url + 'eq null'
        self._filters.append(filter_str)


class ZaakRelationFilter(RelationsFilter):

    @property
    def related_url(self):
        return 'Zaak'

    @property
    def zaak_related_url(self):
        return self.related_url

    def filter_non_empty_zaak(self):
        self._filter_non_empty()

    def filter_empty_zaak(self):
        self._filter_empty()

    def filter_zaak(self, nummer):
        filter_str = "{}/any(z: z/Nummer eq '{}')".format(self.zaak_related_url, nummer)
        self.add_filter_str(filter_str)

    def filter_zaken(self, zaak_numbers):
        filter_str = "{}/any(z:".format(self.zaak_related_url)
        zaak_nummer_strs = []
        for nummer in zaak_numbers:
            zaak_nummer_strs.append("z/Nummer eq '{}'".format(nummer))
        filter_str += ' or '.join(zaak_nummer_strs)
        filter_str += ')'
        self._filters.append(filter_str)

    def _filter_kamerstuk_str(self, volgnummer):
        return '{}/any(z: z/Volgnummer eq {})'.format(self.zaak_related_url, volgnummer)

    def filter_moties(self):
        filter_str = '{}/any(z: z/Soort eq \'{}\')'.format(self.zaak_related_url, 'Motie')
        self._filters.append(filter_str)
