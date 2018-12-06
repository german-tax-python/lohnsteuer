import unittest
import pprint
from modules.lohnsteuer import *
class TestSteuer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_lohnsteuer_function(self):

        # zone 1
        tarif=SteuerTarif2018()
        s=tarif.berechneLohnsteuer(5000)
        self.assertTrue(0 == s)

        # check max tax value for zone 3
        tarif=SteuerTarif2018()
        s=tarif.berechneLohnsteuer(54949) # random value in zone 3
        print("zone 3 max: "+str(s))
        max = 14456.83
        self.assertTrue(14456.83 -1 <= s*12 <= 14456.83+1)

    def test_steuer_kl1(self):

        steuer = Lohnabrechnung_Kl1()
        testset = steuer.useTestfile("test/cases/2018-kl-1-brutto-5026-59.yml")
        brutto =  testset['brutto']['svbrutto']

        steuer.nutzeTarif(testset['meta']['year'])
        steuer.setKinderFreibetraege(testset['meta']['children'])
        steuer.berechnen(brutto)
