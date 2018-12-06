import pprint
import yaml
from modules.helpers import *

class SteuerTarif2018():
    def __init__(self):
        #super()

        with open("data/tarif-2018.yml", 'r') as f:
            self.data = yaml.load(f)

        self.versicherung_gkv = self.data['sozialversicherung']['kv'] # ges. Krankenversicherung
        self.versicherung_rv = self.data['sozialversicherung']['rv'] # Rentenversicherung
        self.versicherung_pflege = self.data['sozialversicherung']['pv']
        self.versicherung_al=self.data['sozialversicherung']['av'] # Arbeislosengeldversicherung
        self.lohnsteuer_solidaritaetszuschlag = self.data['steuer']['solidaritaetszuschlag']
        self.bemessungsgrenze_rv_al = self.data['bemessungsgrenze']['rv']
        self.bemessungsgrenze_gkv_pflege = self.data['bemessungsgrenze']['kv']

    def getVorsorgekostenpauschale(self, zvE):
        return zvE*0.09375+1900

    def getKinderfreibetrag(self, zvE, k):
        return k*3714

    def berechneLohnsteuerMitFreibetrag(self,zvE):

        nach_formel = self.berechneLohnsteuer(zvE)
        print ("zu versteuerndes Bruttoeinkommen: " + str(zvE))
        print("Lohnsteuer ohne Abzüge nach ESt Formel: " + str(nach_formel))


    def berechneLohnsteuer(self,zvE):

        if zvE<=9000:
            return self.zone1(zvE)/12

        elif 9000<zvE<=13996:
            return self.zone2(zvE)/12

        elif 13996<zvE<=54949:
            return self.zone3(zvE)/12

        elif 54949<zvE<=260532:
            return self.zone4(zvE)/12

        else:
            return self.zone5(zvE)/12


    def zone1(self,zvE):
        return 0

    def zone2(self,zvE):
        y = (zvE-9000)/10000
        S = (997.8*y+1400)*y
        return S

    def zone3(self,zvE):
        z = (zvE-13996)/10000
        S = (220.13*z+2397)*z+948.49
        return S

    def zone4(self,zvE):
        S = 0.42*zvE-8621.75
        return S

    def zone5(self,zvE):
        return 0.45*zvE-16437.7


    def get_sv_brutto_rv_al(self,sv_brutto):

        if (sv_brutto>self.bemessungsgrenze_rv_al):
            return self.bemessungsgrenze_rv_al

        else:
            return sv_brutto

    def getSolidaritaetsZuschlag(self):
        return self.lohnsteuer_solidaritaetszuschlag

    def getVorsorgekostenpauschale(self, zvE):

        return zvE*0.09375+1900

    def getKinderfreibetrag(self, zvE, k):
        return k*3714

    def get_sv_brutto_gkv_pflege(self,sv_brutto):

        if (sv_brutto>self.bemessungsgrenze_gkv_pflege):
            return self.bemessungsgrenze_gkv_pflege
        else:
            return sv_brutto
