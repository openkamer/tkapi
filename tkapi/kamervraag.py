from tkapi.document import Document
from tkapi.document import DocumentSoort
from tkapi.zaak import ZaakSoort
import tkapi.util.document


class Kamervraag(Document):
    filter_param = "Soort eq '{}'".format(DocumentSoort.SCHRIFTELIJKE_VRAGEN.value)

    @property
    def antwoord(self):
        return self._related_document_soort(DocumentSoort.ANTWOORD_SCHRIFTELIJKE_VRAGEN)

    @property
    def mededeling_uitstel(self):
        return self._related_document_soort(DocumentSoort.MEDEDELING_UITSTEL_ANTWOORD)

    def _related_document_soort(self, soort: DocumentSoort):
        for zaak in self.zaken:
            if zaak.soort != ZaakSoort.SCHRIFTELIJKE_VRAGEN:
                continue
            for doc in zaak.documenten:
                if doc.soort == soort:
                    return doc
        return None

    @property
    def document_url(self):
        return tkapi.util.document.get_kamervraag_overheidnl_id(self)


class Antwoord(Document):
    filter_param = "Soort eq '{}'".format(DocumentSoort.ANTWOORD_SCHRIFTELIJKE_VRAGEN.value)

    @property
    def document_url(self):
        return tkapi.util.document.get_kamerantwoord_overheidnl_id(self)
