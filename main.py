from tkinter import *
import math

class bod(Label):
    # def __init__(self, x, y):
    #     self.x = x
    #     self.y = y
    pass

class usecka:
    def __init__(self, bod1, bod2):
        self.bod1 = bod1
        self.bod2 = bod2

class kruznica:
    def __init__(self, bod_stredu, bod_obvodu):
        self.bod_stredu = bod_stredu
        self.bod_obvodu = bod_obvodu

class Pridavanie_objektov:
    tuknute_body = []#pre usecky
    pridavam_usecku = False
    pridavam_kruznicu = False

def vzdialenost_dvoch_bodov(a, b):
    return math.sqrt((a.winfo_x() - b.winfo_x())**2 + (a.winfo_y() - b.winfo_y())**2)

def rovnica_priamky_podla_bodov(x1, y1, x2, y2):#vrati a, b, c tak aby priamka bola: ax + by +c = 0
    a = (y1 - y2)/(x1 - x2)
    return a, -1, y1 - a*x1

def cross_product(x1, y1, x2, y2):
    return x1*y2 - x2*y1

def je_to_rovnaky_bod(x1, y1, x2, y2):
    return abs(x1-x2) < 5 and abs(y1-y2) < 5

def zrataj_priesecnik(e, f):
    e1x, e1y, e2x, e2y = e.bod1.winfo_x(), e.bod1.winfo_y(), e.bod2.winfo_x(), e.bod2.winfo_y()
    f1x, f1y, f2x, f2y = f.bod1.winfo_x(), f.bod1.winfo_y(), f.bod2.winfo_x(), f.bod2.winfo_y()
    if isinstance(e, usecka) and isinstance(f, usecka):
        a1,b1,c1 = rovnica_priamky_podla_bodov(e1x, e1y, e2x, e2y)
        a2,b2,c2 = rovnica_priamky_podla_bodov(f1x, f1y, f2x, f2y)
        x = (b1*c2 - b2*c1)/(a1*b2 - a2*b1)
        y = (c1*a2 - c2*a1)/(a1*b2 - a2*b1)
        if ((cross_product(e2x - e1x, e2y - e1y, f1x - e1x, f1y - e1y) > 0) ^ (cross_product(e2x - e1x, e2y - e1y, f2x - e1x, f2y - e1y) > 0)) and ((cross_product(f2x - f1x, f2y - f1y, e1x - f1x, e1y - f1y) > 0) ^ (cross_product(f2x - f1x, f2y - f1y, e2x - f1x, e2y - f1y) > 0)):
            if not je_to_rovnaky_bod(e1x, e1y, x, y) and not je_to_rovnaky_bod(e2x, e2y, x, y) and not je_to_rovnaky_bod(f1x, f1y, x, y) and not je_to_rovnaky_bod(f2x, f2y, x, y):
                return (x,y)
            return -1 # neni to priesecnik, ak to je jeden z koncovych bodov 
        else:
            return -1
    if isinstance(e, kruznica) and isinstance(f, kruznica):
        return -1
    if isinstance(e, usecka) and f.isinstance(f, kruznica):
        return -1
    if isinstance(e, kruznica) and isinstance(f, usecka):
        return -1

def tuknuty_bod(event):
    widget = event.widget
    if widget not in PO.tuknute_body:
        PO.tuknute_body.append(widget)
    pridat_usecku()
    pridat_kruznicu()

def tuknuty_nepriesecnik(event):
    widget = event.widget
    widget.start_pos = (event.x, event.y)
    tuknuty_bod(event)

def dragUpdate(event):
    widget = event.widget
    widget.place(x=widget.winfo_x() - widget.start_pos[0] + event.x, y=widget.winfo_y() - widget.start_pos[1] + event.y, width=10, height=10)
    canvas_update()

def pridat_usecku():
    if len(PO.tuknute_body) == 2 and PO.pridavam_usecku:
        usecky.append(usecka(PO.tuknute_body[0], PO.tuknute_body[1]))
        PO.tuknute_body = []
        PO.pridavam_usecku = False
        canvas_update()

def pridat_kruznicu():
    if len(PO.tuknute_body) == 2 and PO.pridavam_kruznicu:
        kruznice.append(kruznica(PO.tuknute_body[0], PO.tuknute_body[1]))
        PO.tuknute_body = []
        PO.pridavam_kruznicu = False
        canvas_update()

def pridat_bod(x=100, y=100):
    novy_bod = Label(canvas, bg="red")
    canvas.create_window(x,y, window=novy_bod, width=10, height=10)
    novy_bod.bind("<Button-1>", tuknuty_nepriesecnik)
    novy_bod.bind("<B1-Motion>", dragUpdate)
    body.append(bod(novy_bod))

def canvas_update():
    canvas.delete("ciara")

    neexistujuce_priesecniky = []
    for i in range(len(usecky)):
        for j in range(i+1, len(usecky)):
            objekty = (usecky[i], usecky[j])
            priesecnik = zrataj_priesecnik(objekty[0], objekty[1])
            if priesecnik != -1:
                if objekty not in priesecniky:
                    novy_bod = Label(canvas, bg="blue")
                    novy_bod.bind("<Button-1>", tuknuty_bod)
                    priesecniky[objekty] = novy_bod
                    canvas.create_window(priesecnik[0], priesecnik[1], window=novy_bod, width=10, height=10)
                priesecniky[objekty].place(x=priesecnik[0], y=priesecnik[1], width=10, height=10)
            else:
                if objekty in priesecniky:
                    # print(test,"davam nieco uplne prec",priesecniky[objekty])
                    priesecniky[objekty].place(x=1000000, y=1000000, width=10, height=10)
                    neexistujuce_priesecniky.append(priesecniky[objekty])
    
    for usecka in usecky:
        if usecka.bod1 not in neexistujuce_priesecniky and usecka.bod2 not in neexistujuce_priesecniky:
            canvas.create_line(usecka.bod1.winfo_x(), usecka.bod1.winfo_y(), usecka.bod2.winfo_x(), usecka.bod2.winfo_y(), tags="ciara")
            # print(test, "kreslim ciaru")

    for k in kruznice:
        if k.bod_stredu not in neexistujuce_priesecniky and k.bod_obvodu not in neexistujuce_priesecniky:
            radius = vzdialenost_dvoch_bodov(k.bod_stredu, k.bod_obvodu)
            canvas.create_oval(k.bod_stredu.winfo_x() - radius, k.bod_stredu.winfo_y() - radius, k.bod_stredu.winfo_x() + radius, k.bod_stredu.winfo_y() + radius, outline="black", width=2, tags="ciara")

def vyrobit_usecku_btn():
    PO.pridavam_usecku = True
    PO.tuknute_body = []

def vyrobit_kruznicu_btn():
    PO.pridavam_kruznicu = True
    PO.tuknute_body = []

test = 0
body = []
priesecniky = {}#(objekt1, objekt2) : bod
usecky = []
kruznice = []
PO = Pridavanie_objektov()

sirka_obrazovky = 1000
vyska_obrazovky = 800

root = Tk()

root.title("Zapoctak")
root.geometry(str(sirka_obrazovky) + "x" + str(vyska_obrazovky))

btn_pridaj_bod = Button(root, text="Pridaj Bod", command=pridat_bod, bg="lightgray")
btn_pridaj_bod.pack(padx=20, pady=20)

btn_usecka = Button(root, text="usecka", bg="lightgray", command=vyrobit_usecku_btn)
btn_usecka.pack()
btn_kruznica = Button(root, text="kruznica", bg="lightgray", command=vyrobit_kruznicu_btn)
btn_kruznica.pack()

canvas = Canvas(root, width=vyska_obrazovky, height=sirka_obrazovky, bg="#AAD0AA")
pridat_bod(100,100)
pridat_bod(100,200)
pridat_bod(200,100)
pridat_bod(200,200)

canvas.pack(fill="both", expand=True)

mainloop()

"""
bugy:
pretnutie troch objektov v jednom bode je undefined - teda budu tam tri priesecniky, je otazne, ktory bude navrchu, a z ktoreho sa budu kreslit ciary teda

todo:
pridat bodom moznost desatinnych suradnic
priesecniky
usecka neni priamka

blbosticky todo:
zasvietit kliknute body pri kreslini usecok
pridavanie bodov tak, ze kam kliknem sa prida


potencialne divny dizajn:
dufam ze ked zmenim nejaky bod v poli body, tak sa zmeni aj v poli usecky
nepretnuty priesecnik existuje niekde uplne mimo

nahodne divnosti:
ked som tam mal len jednu cast zistovania pretinania useciek, 

specifikacia zapoctaku predbezne:
geogebra
pridavat body, vediet ich posuvat
vediet spravit usecku medzi dvomi bodmi

"""