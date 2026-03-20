class zahadny_bod:
    def __init__(self, typ, *params):
        self.typ = typ
        if typ == "normalny":
            self.state = zakladny_bod(*params)
        if typ == "priesecnik":
            self.state = priesecnik(*params)

    def preznacit(self, pos):
        self.typ = "normalny"
        self.state = zakladny_bod(pos)

class zakladny_bod:
    def __init__(self, pos):
        self.pos = pos

class priesecnik:## moze byt nejaky koncovy bod nejakeho objektu - vtedy si ho pri kresleni vyratam a az potom to nakreslim, na konci kreslenia vyratam priesecniky vsetkym dvojiciam objektov
    def __init__(self, o1, o2, ktory):#objekty ktorych priesecnik to je
        self.ktory = ktory# parameter na rozlisenie priesecnikov ak maju dva objekty dva priesecniky
        self.o1 = o1
        self.o2 = o2

class usecka:
    def __init__(self, A, B):#body koncov
        self.A = A
        self.B = B

class priamka:
    def __init__(self, A, B):
        self.A = A
        self.B = B

class polpriamka:
    def __init__(self, A, B):
        self.A = A
        self.B = B

class kruznica:
    def __init__(self, S, O):#bod stredu, bod obvodu
        self.S = S
        self.O = O

class instrukcia(usecka, kruznica):
    def __init__(self, typ, *params, schovat=False):
        self.typ = typ
        self.schovat = schovat
        if typ == "usecka":
            usecka.__init__(self, *params)
        if typ == "priamka":
            priamka.__init__(self, *params)
        if typ == "polpriamka":
            polpriamka.__init__(self, *params)
        if typ == "kruznica":
            kruznica.__init__(self, *params)

"""
ako to bude fungovat:
vykonam nejaku postupnost instrukcii, tym vzniknu nejake priesecniky - tie chcem vediet zadat ako parametre do instrukcii dalsej iteracie
pridavanie bodu nie je instrukcia - ten bod je len parameter v dalsich instrukciach
"""