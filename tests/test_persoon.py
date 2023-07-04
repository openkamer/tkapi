import datetime

from tkapi.persoon import Persoon
from tkapi.persoon import PersoonReis
from tkapi.persoon import PersoonOnderwijs
from tkapi.persoon import PersoonContactinformatie
from tkapi.persoon import PersoonContactinformatieSoort

from .core import TKApiTestCase


class TestPersoon(TKApiTestCase):

    def get_fred_teeven(self):
        filter = Persoon.create_filter()
        filter.filter_achternaam('Teeven')
        return self.api.get_personen(filter=filter)[0]

    def test_get_personen(self):
        max_items = 66
        personen = self.api.get_personen(max_items=max_items)
        for persoon in personen:
            print('Roepnaam:', persoon.roepnaam)
            print('Volledige naam:', persoon.voornamen, persoon.achternaam)
            # persoon.print_json()
            # if persoon.fractie_lid is not None:
            #     persoon.fractie_lid.print_json()
            #     if persoon.fractie_lid.fractie is not None:
            #         persoon.fractie_lid.fractie.print_json()
        self.assertEqual(max_items, len(personen))

    def test_persoon_get_fracties(self):
        persoon = self.get_fred_teeven()
        fractieleden = persoon.fractieleden
        print(persoon.roepnaam, persoon.achternaam)
        print('fractieleden:', len(fractieleden))
        for lid in persoon.fractieleden:
            print(lid.fractie.naam)
        for fractie in persoon.fracties:
            print(fractie.naam)
        self.assertEqual(4, len(persoon.fracties))

    def test_get_attributes(self):
        persoon = self.get_fred_teeven()
        self.assertEqual('Teeven', persoon.achternaam)
        self.assertEqual('F.', persoon.initialen)
        self.assertEqual('Fred', persoon.roepnaam)
        self.assertEqual('Fredrik', persoon.voornamen)
        self.assertEqual('Oud Kamerlid', persoon.functie)
        self.assertEqual('man', persoon.geslacht)
        self.assertEqual('Nederland', persoon.geboorteland)
        self.assertEqual('Haarlem', persoon.geboorteplaats)
        self.assertEqual(datetime.date(year=1958, month=8, day=5), persoon.geboortedatum)
        self.assertEqual('Hillegom', persoon.woonplaats)
        self.assertEqual('mr.', persoon.titels)
        self.assertEqual('NL', persoon.land)
        self.assertIsNone(persoon.overlijdensdatum)
        self.assertFalse(persoon.overlijdensplaats)
        print(persoon.contact_informaties)

    def test_get_reizen(self):
        persoon = self.get_fred_teeven()
        reizen = persoon.reizen
        self.assertEqual(5, len(reizen))
        self.assertEqual('Helsinki, Finland', reizen[0].bestemming)
        self.assertEqual('Tweede Kamer der Staten-Generaal.', reizen[0].betaald_door)
        for reis in reizen:
            self.assertIsNotNone(reis.bestemming)
            self.assertIsNotNone(reis.end_date_key())

    def test_get_onderwijs(self):
        persoon = self.get_fred_teeven()
        onderwijs = persoon.onderwijs
        self.assertEqual(4, len(onderwijs))
        self.assertEqual('Nederlands- en notarieel recht', onderwijs[0].opleiding_nl)
        for o in onderwijs:
            self.assertIsNotNone(o.opleiding_nl)
            self.assertTrue(o.opleiding_en)
            print(o.plaats)
            self.assertIsNotNone(o.end_date_key())

    def test_get_loopbaan(self):
        persoon = self.get_fred_teeven()
        loopbaan = persoon.loopbaan
        self.assertEqual(6, len(loopbaan))
        self.assertEqual('Officier van Justitie', loopbaan[0].functie)
        for o in loopbaan:
            self.assertIsNotNone(o.functie)
            print(o.omschrijving, o.werkgever, o.omschrijving_en, o.plaats, o.van, o.tot_en_met, o.begin_date_key, o.end_date_key())

    def test_get_geschenken(self):
        persoon = self.get_fred_teeven()
        geschenken = persoon.geschenken
        self.assertEqual(10, len(geschenken))
        self.assertEqual('Ontvangen van de Irakese ambassade een doros je wijn ter waarde van ongeveer €60,--.', geschenken[0].omschrijving)
        for o in geschenken:
            self.assertIsNotNone(o.datum)

    def test_get_nevenfuncties(self):
        persoon = self.get_fred_teeven()
        nevenfuncties = persoon.nevenfuncties
        self.assertEqual(4, len(nevenfuncties))
        self.assertEqual('Deelname in de Raad van advies van het Comité ter vervolging van oorlogsmisdadigers', nevenfuncties[0].omschrijving)


class TestPersoonFilters(TKApiTestCase):

    def get_pechtold(self):
        filter = Persoon.create_filter()
        filter.filter_achternaam('Pechtold')
        return self.api.get_personen(filter=filter)[0]

    def get_teeven(self):
        filter = Persoon.create_filter()
        filter.filter_achternaam('Teeven')
        return self.api.get_personen(filter=filter)[0]

    def test_filter_achternaam(self):
        achternaam = 'Pechtold'
        filter = Persoon.create_filter()
        filter.filter_achternaam(achternaam)
        personen = self.api.get_personen(filter=filter)
        self.assertEqual(1, len(personen))
        persoon = personen[0]
        self.assertEqual(achternaam, persoon.achternaam)

    def test_filter_has_fractiezetel(self):
        n_items = 10
        filter = Persoon.create_filter()
        filter.filter_has_fractiezetel()
        personen = self.api.get_personen(filter=filter, max_items=n_items)
        self.assertEqual(n_items, len(personen))
        for persoon in personen:
            self.assertTrue(persoon.fractieleden)

    def test_filter_ids(self):
        filter = Persoon.create_filter()
        persoon_a = self.get_pechtold()
        persoon_b = self.get_teeven()
        personen_ids = [persoon_a.id, persoon_b.id]
        filter.filter_ids(ids=personen_ids)
        personen = self.api.get_personen(filter=filter)
        self.assertEqual(2, len(personen))

    def test_filter_name_non_unicode(self):
        filter = Persoon.create_filter()
        filter.filter_achternaam("Koşer Kaya")
        personen = self.api.get_personen(filter=filter)
        self.assertEqual(1, len(personen))

    def test_filter_name_bijsterveldt(self):
        filter = Persoon.create_filter()
        filter.filter_achternaam("Bijsterveldt")
        personen = self.api.get_personen(filter=filter)
        self.assertEqual(1, len(personen))
        print(personen[0].achternaam)

    def test_filter_name_ozturk(self):
        filter = Persoon.create_filter()
        filter.filter_achternaam("Öztürk")
        personen = self.api.get_personen(filter=filter)
        self.assertEqual(1, len(personen))
        print(personen[0].achternaam)

    # TODO BR: should this return something?
    # def test_filter_name_pater_postma(self):
    #     filter = Persoon.create_filter()
    #     filter.filter_achternaam("Pater-Postma")
    #     personen = self.api.get_personen(filter=filter)
    #     for persoon in personen:
    #         print(persoon)
    #     print(personen[0].achternaam)
    #     self.assertEqual(1, len(personen))

    def test_filter_name_ormel(self):
        filter = Persoon.create_filter()
        filter.filter_achternaam("Ormel")
        personen = self.api.get_personen(filter=filter)
        for persoon in personen:
            print(persoon)
        print(personen[0].achternaam)
        self.assertEqual(1, len(personen))


class TestPersoonReis(TKApiTestCase):

    def test_get_reis(self):
        max_items = 1
        reizen = self.api.get_reizen(max_items=max_items)
        print(reizen[0].id)
        self.assertEqual(max_items, len(reizen))
        uid = '059ac7ec-c871-4ac4-a604-aaca1d8641a2'
        reis = self.api.get_item(PersoonReis, id=uid)
        self.assertEqual('Londen, Engeland, Stockholm, Zweden en Berlijn, Duitsland', reis.bestemming)
        self.assertEqual('Werkbezoek vaste commissie voor Verkeer en Waterstaat.', reis.doel)
        self.assertEqual('Tweede Kamer der Staten-Generaal.', reis.betaald_door)
        self.assertEqual(datetime.date(2008, 5, 9), reis.tot_en_met)
        self.assertEqual('3f57c8c6-117b-4ef4-a240-d621a8ae7dfb', reis.persoon.id)

    def test_get_reizen(self):
        n_items = 20
        reizen = self.api.get_reizen(max_items=n_items)
        print('reizen:', len(reizen))
        self.assertEqual(n_items, len(reizen))
        for reis in reizen:
            print(reis.id)
            print(reis.bestemming)
            print(reis.doel)
            print(reis.van, reis.tot_en_met)
            print(reis.betaald_door)
            self.assertIsNotNone(reis.bestemming)
            self.assertIsNotNone(reis.doel)
            self.assertIsNotNone(reis.van)
            self.assertIsNotNone(reis.tot_en_met)
            self.assertIsNotNone(reis.betaald_door)

    def test_get_reizen_count(self):
        n_items = 1000
        reizen = self.api.get_reizen(max_items=n_items)
        print('reizen:', len(reizen))
        self.assertEqual(n_items, len(reizen))


class TestPersoonGeschenk(TKApiTestCase):

    def test_get_geschenk(self):
        max_items = 1
        geschenken = self.api.get_geschenken(max_items=max_items)
        print(geschenken[0].id)

    def test_get_geschenken_count(self):
        n_items = 1000
        geschenken = self.api.get_geschenken(max_items=n_items)
        print('geschenken:', len(geschenken))
        self.assertEqual(n_items, len(geschenken))


class TestPersoonOnderwijs(TKApiTestCase):

    def test_get_first(self):
        onderwijs = self.api.get_items(PersoonOnderwijs, max_items=1)[0]
        onderwijs.print_json()
        self.assertTrue(onderwijs.opleiding_nl)
        self.assertTrue(onderwijs.instelling)
        self.assertTrue(onderwijs.persoon.id)


class TestPersoonContactinformatie(TKApiTestCase):

    def test_get_items(self):
        max_items = 50
        contact_infos = self.api.get_items(PersoonContactinformatie, max_items=max_items)
        for info in contact_infos:
            self.assertIn(info.soort, PersoonContactinformatieSoort)
            self.assertIsNotNone(info.persoon)
            self.assertTrue(info.waarde)
            print(info.soort, info.persoon, info.waarde)
