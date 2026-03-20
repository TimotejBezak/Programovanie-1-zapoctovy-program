class zahadny_bod: #je to bud priesecnik alebo bod s konkretnymi suradnicami
    def __init__(self, typ, *params):
        self.typ = typ
        if typ == "normalny":
            self.state = zakladny_bod(*params)
        if typ == "priesecnik":
            self.state = priesecnik(*params)

    def preznacit(self, pos):
        self.typ = "normalny"
        self.state = zakladny_bod(pos)

class zakladny_bod: #bod s konkretnymi suradnicami
    def __init__(self, pos):
        self.pos = pos

class priesecnik: # bod definovany ako priesecnik nejakych dvoch objektov, musim najprv zistit suradnice tych objektov, aby som vedel kde ho mam nakreslit
    def __init__(self, o1, o2, ktory): #objekty ktorych priesecnik to je
        self.ktory = ktory # parameter na rozlisenie priesecnikov ak maju dva objekty dva priesecniky
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
