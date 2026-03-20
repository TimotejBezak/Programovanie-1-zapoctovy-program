from tkinter import *
from instrukcia import instrukcia,zahadny_bod
from kreslenie import kresli
from matematika import vzdialenost_dvoch_bodov

print(TkVersion)
#toto je ten subor, ktory treba spustat
#je tu implementacia pridavania novych bodov, pridavania instrukcii na geometricke konstrukcie

farba_hover_bodu = "yellow"
farba_normalny_bod = "red"
farba_priesecnik = "blue"
default_napoveda = "tukni na nejake tlacidlo"
napoveda_text = {"usecka" : "tukni na dva body", 
                 "priamka" : "tukni na dva body",
                 "polpriamka" : "tukni na dva body",
                 "kruznica" : "tukni na stred, potom na bod na obvode",
                 "os_usecky" : "tukni na koncove body usecky",
                 "os_uhla" : "tukni na nejake tri body, ten druhy ma byt ten pri ktorom je ten uhol",
                 "kolmica" : "tukni na nejaky bod, a potom na nejake dva body urcujuce priamku, nakresli sa kolmica z toho bodu",
                 "rovnobezka" : "tukni na nejaky bod, a potom na nejake dva body urcujuce priamku, nakresli sa rovnobezka cez ten bod"
                 }
class Pridavanie_objektov:
    tuknute_body = [] #aby konstrukcia vedela ktorych bodov sa tyka
    pridavam = {"usecka":False,"polpriamka":False,"priamka":False,"kruznica":False,"os_usecky":False,"os_uhla":False,"kolmica":False,"rovnobezka":False}

def on_enter(event):
    event.widget.config(bg=farba_hover_bodu)

def on_leave_normalny(event):
    event.widget.config(bg=farba_normalny_bod)

def on_leave_priesecnik(event):
    event.widget.config(bg=farba_priesecnik)

def usecka_btn():
    napoveda.config(text=napoveda_text["usecka"])
    vyrobit_objekt("usecka")

def priamka_btn():
    napoveda.config(text=napoveda_text["priamka"])
    vyrobit_objekt("priamka")

def polpriamka_btn():
    napoveda.config(text=napoveda_text["polpriamka"])
    vyrobit_objekt("polpriamka")

def kruznica_btn():
    napoveda.config(text=napoveda_text["kruznica"])
    vyrobit_objekt("kruznica")

def os_usecky_btn():
    napoveda.config(text=napoveda_text["os_usecky"])
    vyrobit_objekt("os_usecky")

def os_uhla_btn():
    napoveda.config(text=napoveda_text["os_uhla"])
    vyrobit_objekt("os_uhla")

def kolmica_btn():
    napoveda.config(text=napoveda_text["kolmica"])
    vyrobit_objekt("kolmica")

def rovnobezka_btn():
    napoveda.config(text=napoveda_text["rovnobezka"])
    vyrobit_objekt("rovnobezka")

def os_usecky_postup(parametre):
    a, b = parametre
    k1 = instrukcia("kruznica", a, b, schovat=True)
    k2 = instrukcia("kruznica", b, a, schovat=True)
    return [k1, k2, instrukcia("priamka", zahadny_bod("priesecnik", k1, k2, 0), zahadny_bod("priesecnik", k1, k2, 1))]

def os_uhla_postup(parametre):
    #kruznica s nahodnym polomerom
    a,b,c = parametre
    bod_obvodu_prvej_kruznice = zahadny_bod("normalny", (-10, -10))#aj tu je to pokazene
    k0 = instrukcia("kruznica", b, bod_obvodu_prvej_kruznice, schovat=True)
    pa = instrukcia("polpriamka", b, a, schovat=True)
    pc = instrukcia("polpriamka", b, c, schovat=True)
    p1 = zahadny_bod("priesecnik", pa, k0, 0)
    p2 = zahadny_bod("priesecnik", pc, k0, 0)
    # skopirovany postup os usecky - mozno to neni idealne, ale tak
    k1 = instrukcia("kruznica", p1, p2, schovat=True)
    k2 = instrukcia("kruznica", p2, p1, schovat=True)
    return [pa, pc, k0, k1, k2, instrukcia("priamka", zahadny_bod("priesecnik", k1, k2, 0), zahadny_bod("priesecnik", k1, k2, 1))]

def kolmica_postup(parametre): #funguje  prvy bod je ten mimo priamky, drune dva su na priamke
    a,b,c = parametre
    bod_obvodu = zahadny_bod("normalny", (2000, 0))#ten bod obvodu sa nemeni  pozor na to aby to nebolo viac ako ta konstanta v kresli pre usecky
    k = instrukcia("kruznica", a, bod_obvodu, schovat=True)
    p = instrukcia("priamka", b, c, schovat=True)
    c1 = zahadny_bod("priesecnik", k, p, 0)
    c2 = zahadny_bod("priesecnik", k, p, 1)
    return [k, p] + os_usecky_postup((c1, c2))

def rovnobezka_postup(parametre): # druhe dva body definuju priamku
    a,b,c = parametre
    kolmica = kolmica_postup((a,b,c))
    g = zahadny_bod("priesecnik", kolmica[-1], kolmica[1], 0)
    return kolmica + kolmica_postup((a, a, g))

# def opisana_kruznica_postup(): to sa mi nechce uz robit
#     return

# def dotycnica_postup():
#     return

def vyrobit_objekt(co):
    for i in PO.pridavam:
        PO.pridavam[i] = False
    PO.pridavam[co] = True
    PO.tuknute_body = []

def tuknuty_bod(event):
    widget = event.widget
    PO.tuknute_body.append(widget)
    pridat_zakladny_objekt("usecka", 2)
    pridat_zakladny_objekt("priamka", 2)
    pridat_zakladny_objekt("polpriamka", 2)
    pridat_zakladny_objekt("kruznica", 2)
    pridat_objekt("os_usecky", 2, os_usecky_postup)
    pridat_objekt("os_uhla", 3, os_uhla_postup)
    pridat_objekt("kolmica", 3, kolmica_postup)
    pridat_objekt("rovnobezka", 3, rovnobezka_postup)

def tuknuty_nepriesecnik(event):
    widget = event.widget
    widget.start_pos = (event.x, event.y)
    tuknuty_bod(event)

def dragUpdate(event):
    widget = event.widget
    novy_pos = (widget.winfo_x() - widget.start_pos[0] + event.x, widget.winfo_y() - widget.start_pos[1] + event.y)
    widget.place(x=novy_pos[0], y=novy_pos[1], width=10, height=10)
    body_canvas[widget].state.pos = novy_pos
    canvas_update()

def pridat_zakladny_objekt(co, pocet_bodov):
    if len(PO.tuknute_body) == pocet_bodov and PO.pridavam[co]:
        instrukcie.append(instrukcia(co, body_canvas[PO.tuknute_body[0]], body_canvas[PO.tuknute_body[1]]))
        PO.tuknute_body = []
        PO.pridavam[co] = False
        canvas_update()
        napoveda.config(text=default_napoveda)
    
def pridat_objekt(co, pocet_bodov, postup_rysovania):
    if len(PO.tuknute_body) == pocet_bodov and PO.pridavam[co]:
        body = []
        for i in range(pocet_bodov):
            body.append(body_canvas[PO.tuknute_body[i]])
        for i in postup_rysovania(body):
            instrukcie.append(i)
        PO.tuknute_body = []
        PO.pridavam[co] = False
        canvas_update()
        napoveda.config(text=default_napoveda)


def canvas_update():
    canvas.delete("ciara")
    cervene_body = []
    for a in body_canvas:
        c = body_canvas[a]
        if c.typ == "normalny":
            cervene_body.append(c)
    usecky, kruznice, priesecniky = kresli(instrukcie, cervene_body)
    for u in usecky:
        canvas.create_line(u[0][0]+5, u[0][1]+5, u[1][0]+5, u[1][1]+5, tags="ciara")
    for k in kruznice:
        radius = vzdialenost_dvoch_bodov(k[0], k[1])
        canvas.create_oval(k[0][0] - radius+5, k[0][1] - radius+5, k[0][0] + radius+5, k[0][1] + radius+5, outline="black", width=2, tags="ciara")

    mam_nakreslit = set()
    for pos, p in priesecniky:
        mam_nakreslit.add(p)
        if p in priesecniky_label:
            priesecniky_label[p].place(x=pos[0], y=pos[1], width=10, height=10)
        else:
            novy_bod = Label(canvas, bg=farba_priesecnik) #modry
            novy_bod.bind("<Button-1>", tuknuty_bod) #to je ta funkcia na pridavanie useciek a kruznic
            novy_bod.bind("<Enter>", on_enter)
            novy_bod.bind("<Leave>", on_leave_priesecnik)
            canvas.create_window(pos[0], pos[1], window=novy_bod, width=10, height=10)
            novy_bod.place(x=pos[0], y=pos[1], width=10, height=10)
            priesecniky_label[p] = novy_bod
        if p not in body_canvas:
            body_canvas[priesecniky_label[p]] = p

    for p in priesecniky_label:
        if p not in mam_nakreslit: #nemam ho kreslit
            priesecniky_label[p].place(x=100000, y=0, width=10, height=10) #nakreslim ho niekde fuc

def pridat_bod(x=100, y=100):
    novy_bod = Label(canvas, bg=farba_normalny_bod)
    canvas.create_window(x,y, window=novy_bod, width=10, height=10)
    novy_bod.place(x=x, y=y, width=10, height=10)
    novy_bod.bind("<Button-1>", tuknuty_nepriesecnik)
    novy_bod.bind("<B1-Motion>", dragUpdate)
    novy_bod.bind("<Enter>", on_enter)
    novy_bod.bind("<Leave>", on_leave_normalny)
    body_canvas[novy_bod] = zahadny_bod("normalny",(x,y))

PO = Pridavanie_objektov()
instrukcie = []# bude obsahovat aj body
body_canvas = {}# Label: zahadnybod   tu budu aj priesecniky
priesecniky_label = {}# zahadnybodpriesecnik : Label

sirka_obrazovky = 1000
vyska_obrazovky = 800

root = Tk()

root.title("Zapoctak")
root.geometry(str(sirka_obrazovky) + "x" + str(vyska_obrazovky))

btn_pridaj_bod = Button(root, text="Pridaj Bod", command=pridat_bod, bg="lightgray")
btn_pridaj_bod.grid(row=0,column=0)

napoveda = Label(root, text=default_napoveda)
napoveda.grid(row=0, column=1, columnspan=7)

btn_usecka = Button(root, text="usecka", bg="lightgray", command=usecka_btn)
btn_usecka.grid(row=1,column=0)
btn_priamka = Button(root, text="priamka", bg="lightgray", command=priamka_btn)
btn_priamka.grid(row=1,column=1)
btn_polpriamka = Button(root, text="polpriamka", bg="lightgray", command=polpriamka_btn)
btn_polpriamka.grid(row=1,column=2)
btn_kruznica = Button(root, text="kruznica", bg="lightgray", command=kruznica_btn)
btn_kruznica.grid(row=1,column=3)

btn_os_usecky = Button(root, text="os_usecky", bg="lightgray", command=os_usecky_btn)
btn_os_usecky.grid(row=1,column=4)
btn_os_uhla = Button(root, text="os_uhla", bg="lightgray", command=os_uhla_btn)
btn_os_uhla.grid(row=1,column=5)
btn_kolmica = Button(root, text="kolmica", bg="lightgray", command=kolmica_btn)
btn_kolmica.grid(row=1,column=6)
btn_rovnobezka = Button(root, text="rovnobezka", bg="lightgray", command=rovnobezka_btn)
btn_rovnobezka.grid(row=1,column=7)


canvas = Canvas(root, width=vyska_obrazovky, height=sirka_obrazovky, bg="#AAD0AA")
pridat_bod(200,10)
pridat_bod(100,50)
pridat_bod(300,180)
pridat_bod(100,310)

canvas.grid(row=2,column=0, columnspan=8)#.pack(fill="both", expand=True)

mainloop()