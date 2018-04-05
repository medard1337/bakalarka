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
filtered_list=[]

#tato funkcia premiena string na float
def tofloat(string):
	if (string):
		return float(string)
	return 0.0
t1 = time.time()

#invertor osi
inverter = str(input("Aky format maju vstupne udaje? (A)Napatie/Deformacia alebo (B)Deformacia/Napatie?(A/B)\n"))

filtered_list = []

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

		if (10 < napatie < 2500000 ):
			filtered_list.append([napatie, deformacia])

		sigma.append(napatie)
		delta.append(deformacia)
		graf_list.append([deformacia,napatie])
		if deformacia == 0:
			print('Error: Division by zero\nStlpce vo vstupnom subore su pravdepodobne vymenene.')
			sys.exit(0)
		else:
			points.append(napatie/deformacia)
		

anal = np.array(filtered_list)
sigma_alfa, delta_alfa = anal.T



#deklaruje premennu data v ktorej su hodnoty z points zoradene do radu
data = np.array(graf_list)
#transponuje maticu data
x,y = data.T
#kresli scatter graf z matice data
plt.scatter(x,y,s=0.5)
#print(data)

#linearna regresia
#pre funkciu y = kx + q
xds=round(len(delta_alfa)/10)
xs = np.array(delta_alfa[:xds])
ys = np.array(sigma_alfa[:xds])
#print(xs)


klz_pocitadlo = True
klz = 0
#tato funkcia najde youngov modul pruznosti pre kazdy point a porovna ho s nasledujucim 
for i, vydelene in enumerate(points):
	if vydelene ==0:
		pass
	else:
		if i>=len(points)-1:
			pass
		else:
			if(abs(vydelene-points[i+1]))/vydelene <= 0.05:
				klz = 0
			else:
				klz = klz + 1
				if klz == 10 and klz_pocitadlo == True:
					klz_pocitadlo = False
					medza_klzu = sigma[i]
					young = points[0:i]
					helper = i




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

regres2=(sum(young)/helper)
k,q = fitovanie_smernica_a_intercept(xs,ys)
print('k = ', k, 'q = ', q)
krivka_regresie = [(k*x)+q for x in xs]
#r_squared = koeficient_determinantu(ys, krivka_regresie)
#print('r^2 = ', r_squared)
print('\n---------------------------------\n Modul pruznosti 1 :',round((((sum(young))/helper)/100000),3),'\n---------------------------------\n')
print('\n---------------------------------\n Modul pruznosti 2 :',round(k/100000,3),'\n---------------------------------\n')
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
plt.plot(xs, krivka_regresie,"r--")
plt.show()