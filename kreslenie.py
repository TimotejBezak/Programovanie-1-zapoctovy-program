import copy
from instrukcia import instrukcia
from instrukcia import zahadny_bod, priesecnik
from matematika import usecka_usecka_priesecnik, predlz_usecku_donekonecna, kruznica_kruznica_priesecnik, kruznica_usecka_priesecnik, je_to_rovnaky_bod

def okresat_priesecniky_o_tie_co_su_na_cervenych_bodoch(pozicie):
    if pozicie == -1:
        return -1
    ret = []
    for i in pozicie:
        pridat = True
        for cer in cervene_body:
            if je_to_rovnaky_bod(cer.state.pos[0], cer.state.pos[1], i[0], i[1]):
                pridat = False
        if pridat:
            ret.append(i)
    return ret

def zisti_suradnice_priesecnika(objekt1, objekt2): #vrati tuple dvojic suradnic (priesecnikov moze byt aj viac) alebo -1
    #spolieham sa na to, ze vsetky body toho comu ratam priesecnik su konkretne hodnoty, nie priesecniky
    #ak tomuto priesecniku zmenim potom hodnoty tak, aby to bol normalny bod, tak to bude sediet do buducna
    objekt1, objekt2 = copy.deepcopy(objekt1), copy.deepcopy(objekt2) # toto nic nepokazi, lebo teraz urcite nechcem menit veci tym objektom tak aby si to niekto vsimol
    if objekt1.typ > objekt2.typ: #objekty budu utriedene podla typov
        objekt1, objekt2 = objekt2, objekt1
    vyries_priamky(objekt1, objekt2) # skonvertuje vsetky priamky na usecky
    
    if objekt1.typ == "usecka" and objekt2.typ == "usecka":
        if objekt1.A.state.pos == -1 or objekt1.B.state.pos == -1 or objekt2.A.state.pos == -1 or objekt2.B.state.pos == -1:
            return -1 # jeden z bodov je priesecnik niecoho a nie je definovany
        return usecka_usecka_priesecnik((objekt1.A.state.pos, objekt1.B.state.pos), (objekt2.A.state.pos, objekt2.B.state.pos))
    
    if objekt1.typ == "kruznica" and objekt2.typ == "usecka":
        if objekt1.S.state.pos == -1 or objekt1.O.state.pos == -1 or objekt2.A.state.pos == -1 or objekt2.B.state.pos == -1:
            return -1
        return kruznica_usecka_priesecnik((objekt1.S.state.pos, objekt1.O.state.pos), (objekt2.A.state.pos, objekt2.B.state.pos))
    
    if objekt1.typ == "kruznica" and objekt2.typ == "kruznica":
        if objekt1.S.state.pos == -1 or objekt1.O.state.pos == -1 or objekt2.S.state.pos == -1 or objekt2.O.state.pos == -1:
            return -1
        return kruznica_kruznica_priesecnik((objekt1.S.state.pos, objekt1.O.state.pos), (objekt2.S.state.pos, objekt2.O.state.pos))

def vyries_priamky(objekt1, objekt2):
    O = [objekt1, objekt2]
    for i in range(2):
        if O[i].typ == "priamka":
            O[i].typ = "usecka"
            O[i].A.state.pos, O[i].B.state.pos = predlz_usecku_donekonecna(O[i].A.state.pos, O[i].B.state.pos) #pozor je to nahoda ze priamka aj usecka pomenuva koncove body rovnako
        if O[i].typ == "polpriamka":
            O[i].typ = "usecka"
            _, O[i].B.state.pos = predlz_usecku_donekonecna(O[i].A.state.pos, O[i].B.state.pos)

def skonvertuj_na_suradnice(bod):
    if bod.typ == "priesecnik":
        pozicie = zisti_suradnice_priesecnika(bod.state.o1, bod.state.o2)
        if pozicie == -1 or bod.state.ktory > len(pozicie)-1:
            bod.preznacit(-1) # neexistujuce priesecniky budu mat pos=-1
            return -1
        bod.preznacit(pozicie[bod.state.ktory])#tuple index out of range
    return 0

priesecnik_objekty = {}
cervene_body = []
def kresli(instrukcie_in, cervene_body_in):#instrukcie je pole instrukcii - bud zakladne body alebo usecky alebo kruznice - tie mozu mat v parametroch priesecnik namiesto konkretneho bodu
    global priesecnik_objekty, cervene_body
    priesecniky_zakaz_zobrazit = []
    cervene_body = cervene_body_in
    instrukcie = copy.deepcopy(instrukcie_in) # nech si tie priesecniky nepokazim do dalsej iteracie
    # priamky chcem skonvertovat na usecky len pre ucely ratania priesecnikov a pre ucely kreslenia tej konkretnej priamky
    ret_usecky = []
    ret_kruznice = []
    for i in instrukcie:
        if i.typ == "usecka":
            a = skonvertuj_na_suradnice(i.A)
            b = skonvertuj_na_suradnice(i.B)
            if a != -1 and b != -1 and not i.schovat: #musia existovat obidva priesecniky nato aby sa to dalo nakreslit
                ret_usecky.append((i.A.state.pos, i.B.state.pos))
        if i.typ == "priamka":
            a = skonvertuj_na_suradnice(i.A)
            b = skonvertuj_na_suradnice(i.B)
            if a != -1 and b != -1 and not i.schovat:
                ret_usecky.append(predlz_usecku_donekonecna(i.A.state.pos, i.B.state.pos))
        if i.typ == "polpriamka":
            a = skonvertuj_na_suradnice(i.A)
            b = skonvertuj_na_suradnice(i.B)
            if a != -1 and b != -1 and not i.schovat:
                ret_usecky.append((i.A.state.pos, predlz_usecku_donekonecna(i.A.state.pos, i.B.state.pos)[1]))
        if i.typ == "kruznica":
            a = skonvertuj_na_suradnice(i.S)
            b = skonvertuj_na_suradnice(i.O)
            if a != -1 and b != -1 and not i.schovat:
                ret_kruznice.append((i.S.state.pos, i.O.state.pos))

    ret_priesecniky = []# (pozicia, zahadnybod priesecnik)  pozicie kam mam nakreslit priesecnik - ale k tomu objektu si chcem pametat aj to ze coho je priesecnik
    for k in range(len(instrukcie)):
        for l in range(k+1, len(instrukcie)):
            i, j = instrukcie_in[k], instrukcie_in[l] # aby to bol ten isty objekt vzdy
            pozicie = zisti_suradnice_priesecnika(instrukcie[k], instrukcie[l]) # tu mam vyratane tie priesecniky uz
            pozicie = okresat_priesecniky_o_tie_co_su_na_cervenych_bodoch(pozicie)
            if pozicie != -1:
                for q in range(len(pozicie)): #sfunkcnene pre viac priesecnikov
                    if not i.schovat and not j.schovat:
                        if (i,j,q) not in priesecnik_objekty:
                            priesecnik_objekty[(i,j,q)] = zahadny_bod("priesecnik", i, j, q)
                        if (i, j, q) not in priesecniky_zakaz_zobrazit and (j, i, q) not in priesecniky_zakaz_zobrazit:
                            ret_priesecniky.append((pozicie[q], priesecnik_objekty[(i,j,q)]))

    return (ret_usecky, ret_kruznice, ret_priesecniky)