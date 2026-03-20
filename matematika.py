import math

def vzdialenost_dvoch_bodov(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def rovnica_priamky_podla_bodov(x1, y1, x2, y2):#vrati a, b, c tak aby priamka bola: ax + by +c = 0
    if x1 - x2 == 0:
        a = 1000000000
    else:
        a = (y1 - y2)/(x1 - x2)
    return a, -1, y1 - a*x1

def cross_product(x1, y1, x2, y2):
    return x1*y2 - x2*y1

def je_to_rovnaky_bod(x1, y1, x2, y2):
    return abs(x1-x2) < 5 and abs(y1-y2) < 5

def predlz_usecku_donekonecna(pos1, pos2):# suradnice koncovych bodov
    ex, ey, fx, fy = pos1[0], pos1[1], pos2[0], pos2[1]
    vela = 10000
    if ex == fx: #vertikalna usecka
        if ey < fy:
            return ((ex, -vela), (fx, vela))
        else:
            return ((fx, vela), (ex, -vela))
    else:
        a,b,c = rovnica_priamky_podla_bodov(ex, ey, fx, fy)
        ret = ((-vela, -(a*(-vela)+c)/b), (vela, -(a*vela+c)/b))
        if ex < fx:
            return ret
        return (ret[1], ret[0])

def lezi_bod_na_usecke_ak_viem_ze_lezi_na_priamke_tej_usecky(u, bod):# tuple dvojic suradnic koncovych bodov usecky, suradnice bodu
    ex, ey, fx, fy = u[0][0], u[0][1], u[1][0], u[1][1]
    if ex == fx:
        return min(ey, fy) <= bod[1] <= max(ey, fy) 
    return min(ex, fx) <= bod[0] <= max(ex, fx)

def usecka_usecka_priesecnik(e, f): # vraciam to ako -1 alebo tuple velkosti 1 s s dvojicou suradnic
    e1x, e1y, e2x, e2y = e[0][0], e[0][1], e[1][0], e[1][1]
    f1x, f1y, f2x, f2y = f[0][0], f[0][1], f[1][0], f[1][1]
    a1,b1,c1 = rovnica_priamky_podla_bodov(e1x, e1y, e2x, e2y)
    a2,b2,c2 = rovnica_priamky_podla_bodov(f1x, f1y, f2x, f2y)
    if(a1*b2 - a2*b1 == 0):
        return -1 # delenie nulou
    x = (b1*c2 - b2*c1)/(a1*b2 - a2*b1)
    y = (c1*a2 - c2*a1)/(a1*b2 - a2*b1)
    if ((cross_product(e2x - e1x, e2y - e1y, f1x - e1x, f1y - e1y) > 0) ^ (cross_product(e2x - e1x, e2y - e1y, f2x - e1x, f2y - e1y) > 0)) and ((cross_product(f2x - f1x, f2y - f1y, e1x - f1x, e1y - f1y) > 0) ^ (cross_product(f2x - f1x, f2y - f1y, e2x - f1x, e2y - f1y) > 0)):
        if not je_to_rovnaky_bod(e1x, e1y, x, y) and not je_to_rovnaky_bod(e2x, e2y, x, y) and not je_to_rovnaky_bod(f1x, f1y, x, y) and not je_to_rovnaky_bod(f2x, f2y, x, y):
            return ((x,y),)
        return -1 # neni to priesecnik, ak to je jeden z koncovych bodov 
    else:
        return -1

def kruznica_usecka_priesecnik(k, u):
    ex, ey, fx, fy = u[0][0], u[0][1], u[1][0], u[1][1]
    sx, sy, ox, oy = k[0][0], k[0][1], k[1][0], k[1][1]
    kandidati = kruznica_priamka_priesecnik(k, u)
    if kandidati == -1:
        return -1
    ret = []
    for kandidat in kandidati: #overim ci su na tej usecke
        if lezi_bod_na_usecke_ak_viem_ze_lezi_na_priamke_tej_usecky(u, kandidat):
            ret.append(kandidat)
    return tuple(ret)

def kruznica_priamka_priesecnik(k, u):
    ex, ey, fx, fy = u[0][0], u[0][1], u[1][0], u[1][1]
    sx, sy, ox, oy = k[0][0], k[0][1], k[1][0], k[1][1]
    ex -= sx
    ey -= sy
    fx -= sx
    fy -= sy # posuniem to tak, aby kruznica mala stred v pociatku
    a,b,c = rovnica_priamky_podla_bodov(ex, ey, fx, fy)
    r = vzdialenost_dvoch_bodov((sx,sy),(ox,oy))
    # TODO ak b=0
    diskriminant = 4*c**2*a**2/b**4 - 4 * (1+a**2/b**2) * (c**2/b**2-r**2)
    if diskriminant < 0:
        return -1
    if diskriminant == 0:#jeden priesecnik
        return -1 #nieco
    x1 = (-2*c*a/b**2+math.sqrt(diskriminant))/(2*(1+a**2/b**2))
    x2 = (-2*c*a/b**2-math.sqrt(diskriminant))/(2*(1+a**2/b**2))
    y1 = (-c-a*x1)/b
    y2 = (-c-a*x2)/b
    x1 += sx
    x2 += sx
    y1 += sy
    y2 += sy
    return ((x1, y1), (x2, y2))#priesecniky s priamkou tej usecky

def kruznica_kruznica_priesecnik(l, k):
    s1x, s1y, o1x, o1y = l[0][0], l[0][1], l[1][0], l[1][1]
    s2x, s2y, o2x, o2y = k[0][0], k[0][1], k[1][0], k[1][1]
    r1, r2 = vzdialenost_dvoch_bodov((s1x, s1y), (o1x, o1y)), vzdialenost_dvoch_bodov((s2x, s2y), (o2x, o2y))
    ## robim posunutie (-s1x, -s1y) a rotaciu -atan(s2y/s2x)
    s2x -= s1x #posunutie
    s2y -= s1y
    if s2x == s2y == 0:
        return -1
    uhol = math.atan2(s2y,s2x)
    s2x = vzdialenost_dvoch_bodov((0,0), (s2x, s2y)) #rotacia

    if s2x > r1+r2 or s2x + r2 < r1 or s2x + r1 < r2:
        return -1
    if s2x == r1+r2:
        x, y = r1, 0
        novy_x = x*math.cos(uhol) - y*math.sin(uhol)
        novy_y = x*math.sin(uhol) + y*math.cos(uhol)    
        x, y = novy_x, novy_y
        x += s1x
        y += s1y
        return (x, y) #zrotovane a posunute
    x = 0.5*(-r2**2 + r1**2 + s2x**2)/s2x
    y = math.sqrt(max(0, r1**2-x**2)) # ono to vie byt malinko zaporne kvoli nepresnostiam
    y2 = -y
    novy_x = x*math.cos(uhol) - y*math.sin(uhol) #inverzna rotacia
    novy_y = x*math.sin(uhol) + y*math.cos(uhol)
    novy_x2 = x*math.cos(uhol) - y2*math.sin(uhol) #inverzna rotacia
    novy_y2 = x*math.sin(uhol) + y2*math.cos(uhol)
    x, y, x2, y2 = novy_x, novy_y, novy_x2, novy_y2
    x += s1x #inverzne posunutie
    y += s1y
    x2 += s1x
    y2 += s1y
    return ((x,y),(x2,y2))