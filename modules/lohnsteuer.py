import pprint
import yaml

from modules.steuertarif import *
from modules.helpers import *
from prettytable import PrettyTable

class Lohnabrechnung_Kl1:

        def __init__(self):
            self.bruttogehalt = 0
            self.kinderfreibetrag = 0
            self.monatlich_abschlag = 0
            self.lohnsteuerermaessigung=0
            self.abzugArbeitgeberMonatBrutto = 0
            self.abzugArbeitgeberMonatNetto = 0

            self.weihnachtsgeld=0
            self.zuschussMonat=0
            self.zuschussJahr=0

            self.lohnsteuer=0
            self.netto=0

            self.tarif = None
            self.gkv_abgabe=0

            self.testfile= None
            self.testdata = None

            # report configuration
            columns=["Position","Value","Test","Control"]
            self.t_report = PrettyTable(columns)
            self.t_report.align["Position"]="l"
            self.t_report.align["Value"]="r"
            self.t_report.align["Control"]="r"
            self.mainAssert = True

        def add_row(self, index, value):

            # index -> foo-bar <- split by hyphen
            if "-" in index:
                array = index.split("-")
                block = array[0]
                item = array[1]
                control_value = self.testdata[block][item]
            else:
                control_value = self.testdata[index]

            test="?"
            value = fmt_money2(value)
            if control_value == value:
                test = " OK "
            else:
                self.mainAssert = False
                test = " ! "

            self.t_report.add_row([index,value,test,control_value])



        def setLohnsteuerermaessigung(self,x):
            self.lohnsteuerermaessigung=x

        def setAbzugArbeitgeberMonatBrutto(self,x):
            self.abzugArbeitgeberMonatBrutto=x

        def setAbzugArbeitgeberMonatNetto(self,x):
            self.abzugArbeitgeberMonatNetto=x

        def nutzeTarif(self,jahr):
            if jahr <= 2018:
                self.tarif=SteuerTarif2018()

            elif jahr == 2019:
                self.tarif=SteuerTarif2019()

            else:
                self.tarif=SteuerTarif2020()


        def setKinderFreibetraege(self, freibetrag):
            self.kinderfreibetrag=freibetrag

        def calcLohnsteuer(self):
            return steuer

        def setMonatlichAbschlag(self,abschlag):
            self.monatlich_abschlag = abschlag


        def getNettoMonat(self):
            return self.netto

        def getLohnsteuerMonat(self):
            return self.lohnsteuer


        def setWeihnachtsgeld(self, x):
            self.weihnachtsgeld=x

        def setZuschussJahr(self,x):
            self.zuschussJahr = x

        def setZuschussMonatBrutto(self,x):
            self.zuschussMonat=x

        def berechnen(self, brutto,  steuerklasse=1,  print_report = False):

            self.bruttogehalt = brutto
            b = brutto

            st_brutto = self.bruttogehalt + self.abzugArbeitgeberMonatBrutto+self.zuschussMonat*0.90905
            sv_brutto = self.bruttogehalt+self.zuschussMonat
            if print_report:
                print("zu verst. Monatsbrutto: " + str(fmt_money(self.bruttogehalt)))

            if print_report:
                print("SV BRUTTO: " + str(fmt_money(sv_brutto)))

            if print_report:
                print("ST BRUTTO: " + str(fmt_money(st_brutto)))

            jahresbrutto = 12*st_brutto
            zvE =12*st_brutto
            vspsch = self.tarif.getVorsorgekostenpauschale(jahresbrutto)
            kinderfreibetrag = self.tarif.getKinderfreibetrag(zvE,self.kinderfreibetrag)

            #if print_report:
            #    print("Kinderfreitrag: " + "/"+ str(self.kinderfreibetrag) +"/ :" + str(kinderfreibetrag))

            if print_report:
                print("zu verst. Jahresbrutto: " + str(fmt_money(jahresbrutto)))

            if print_report:
                print("Lohnsteuer ohne Freibeträge: " + str(fmt_money(self.tarif.berechneLohnsteuer(jahresbrutto))))

            zvE = zvE-self.tarif.data['freibetrag']['werbungskostenpauschale'] # Werbungskostenpauschale
            zve = zvE - self.tarif.data['freibetrag']['sonderausgabenpauschale'] # Sonderausgabenpauschale
            zvE = zvE - vspsch  # Vorsorgekostenpauschale
            zvE = zvE - kinderfreibetrag
            zvE = zvE - self.lohnsteuerermaessigung

            if print_report:
                print("zu verst. Jahresbrutto abgl. aller Freibeträge: " + str(fmt_money(zvE)))

            lohnsteuer = self.tarif.berechneLohnsteuer(zvE)

            if print_report:
                print("Lohnsteuer-Abgabe mtl.: " + str(lohnsteuer))

            abzug_gkv = self.tarif.get_sv_brutto_gkv_pflege(sv_brutto)*(self.tarif.versicherung_gkv/100)
            abzug_pflege = self.tarif.get_sv_brutto_gkv_pflege(sv_brutto)*(self.tarif.versicherung_pflege/100)
            self.gkv_abgabe=abzug_gkv

            abzug_rv = self.tarif.get_sv_brutto_rv_al(sv_brutto)*(self.tarif.versicherung_rv/100)
            abzug_al = self.tarif.get_sv_brutto_rv_al(sv_brutto)*(self.tarif.versicherung_al/100)

            soli=self.tarif.getSolidaritaetsZuschlag()*lohnsteuer/100

            netto = self.bruttogehalt - (abzug_gkv + abzug_rv + abzug_al + abzug_pflege + lohnsteuer+soli)

            netto = netto-self.abzugArbeitgeberMonatNetto

            self.add_row("brutto-svbrutto", sv_brutto)

            self.add_row("sozialversicherung-kv", abzug_gkv)
            self.add_row("sozialversicherung-rv", abzug_rv)
            self.add_row("sozialversicherung-av", abzug_al)
            self.add_row("sozialversicherung-pv", abzug_pflege)

            self.add_row("freibetrag-kinderfreibetrag", kinderfreibetrag)
            self.add_row("freibetrag-versorgungspauschale", vspsch)

            self.add_row("steuer-soli", soli)
            self.add_row("steuer-lohnsteuer", lohnsteuer)
            self.add_row("netto", netto)

            if print_report:
                print("Netto: " + str(fmt_money(netto)))


            if print_report is True or self.mainAssert is False:
                print(self.t_report)

            assert self.mainAssert is True
            self.netto = netto
            return self.netto

        def inRange(self,wert,abweichung):
            return wert-abweichung<=abweichung<=wert+abweichung

        def getNettoJahr(self):
            return self.netto*12


        def useTestfile(self, file):
            self.testfile = file
            with open(self.testfile, 'r') as f:
                self.testdata = yaml.load(f)

            return self.testdata
