import pylab as pl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from pathlib import Path
from math import ceil
import decimal
import collections
import sys, traceback
import time
from statistics import mean


#otvori subor
filename=input('Enter filename ')
rawfile = open(filename, 'r')
#deklaruje prazdny list s nazvom points
points = []
vydelene = []
sigma = []
delta = []
graf_list = []
sigma_alfa = []
delta_alfa = []
napatie = []
deformacia = []
splitter = []
penor = []

#tato funkcia premiena string na float
def tofloat(string):
	if (string):
		return float(string)
	return 0.0
t1 = time.time()

#invertor osi
inverter = str(input("Aky format maju vstupne udaje? (A)Napatie/Deformacia alebo (B)Deformacia/Napatie?(A/B)\n"))


#tato funkcia prechadza input subor riadok po riadku
for l in rawfile:
	#ak je v riadku viac ako 0 znakov a nezacina sa "
	if len(l) > 0 and not l.startswith('"'):
		#odstrani \n -> symboly noveho riadku a znamienka
		l.rstrip("\n ")
		l.rstrip(",")
		l.rstrip(" ")
		l.rstrip("0.0")
		#rozdeli hodnoty tam kde su rozdelene tabulatorom
		split = l.split('\t')
		if inverter in['A','a']:
			napatie = tofloat(split[0])
			deformacia = tofloat(split[1])
		elif inverter in['B','b']:
			napatie = tofloat(split[1])
			deformacia = tofloat(split[0])
		else:
			print('Zly vyber, kokot')
		
		
		sigma_alfa.append(napatie)
		delta_alfa.append(deformacia)
		graf_list.append([deformacia,napatie])

print(type(sigma_alfa))

#print(graf_list[0])
#points = [(b,a) for (a,b) in graf_list if  a<2500000  and b>0]
#print(points[0])
#points = [(a/b) for (a,b) in points if 40000 < a/b < 250000]




#deklaruje premennu data v ktorej su hodnoty z points zoradene do radu
data = np.array(graf_list)
#transponuje maticu data
x,y = data.T
#kresli scatter graf z matice data
plt.scatter(x,y,s=0.5)
#print(data)

#linearna regresia
#pre funkciu y = kx + q
xds=round(len(delta_alfa)/3)
xs = np.array(delta_alfa[:xds])
ys = np.array(sigma_alfa[:xds])
#print(xs)


def fitovanie_smernica_a_intercept(xs,ys):
	k = (((mean(xs) * mean(ys)) - mean(xs*ys)) / ((mean(xs)**2) - mean(xs**2)))
	q = mean(ys) - k*mean(xs)
	return k,q
	
#definovanie r^2 
#def squared_error(ys_povodne, ys_priamkove):
#	return sum(ys_priamkove-ys_povodne)
	
#koeficient determinantu r^2
#def koeficient_determinantu(ys_povodne,ys_priamkove):
#	y_mean_priamkove = [mean(ys_povodne) for y in ys_povodne]
#	squared_error_regresie = squared_error(ys_povodne, ys_priamkove)
#	squared_error_y_mean = squared_error(ys_povodne, y_mean_priamkove)
#	return 1 - (squared_error_regresie / squared_error_y_mean)
	
k,q = fitovanie_smernica_a_intercept(xs,ys)
print('k = ', k, 'q = ', q)
krivka_regresie = [(k*x)+q for x in xs]
#r_squared = koeficient_determinantu(ys, krivka_regresie)
#print('r^2 = ', r_squared)

t2=time.time()
print(t2-t1,'[s]---- trvanie\n')
from scipy.interpolate import *
#toto fituje krivku k bodom.
fit=np.polyfit(x,y,15)
p=np.poly1d(fit)
p.order
plt.title('Ťahový diagram')
plt.xlabel('deformacia')
plt.ylabel('napatie')
#plt.plot(x,p(x),"r--")
plt.plot(xs, krivka_regresie,"r--")
plt.show()



