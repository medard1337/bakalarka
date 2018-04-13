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


#Otvori subor zadany uzivatelom
filename=input('Enter filename ')
rawfile = open(filename, 'r')

#deklaracia prazdnych listov
points = []
vydelene = []
sigma = []
delta = []
graf_list = []
sigma_alfa = []
delta_alfa = []
napatie = []
deformacia = []
filtered_list=[]


#tato funkcia premiena string na float
def tofloat(string):
	if (string):
		return float(string)
	return 0.0

#timer
t1 = time.time()

#deklaracia premennej na invertovanie osi
inverter = str(input("Aky format maju vstupne udaje? (A)Napatie/Deformacia alebo (B)Deformacia/Napatie?(A/B)\n"))


#tento cyklus prechadza subor riadok po riadku a spracuva ho do citalnej podoby pre program
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

		if (10 < napatie < 2500000 and deformacia > 0 ):
			filtered_list.append([napatie, deformacia])


		sigma.append(napatie)
		delta.append(deformacia)
		graf_list.append([deformacia,napatie])
		#if deformacia == 0:
		#	print('si kokot ty kokot')
		#	sys.exit(0)
		#else:
		#	points.append(napatie/deformacia)
		#points=[filtered_list[0]/filtered_list[1]]


#points=[filtered_list[0],filtered_list[1]]
#transponovanie matice filtered_list
anal = np.array(filtered_list)
sigma_alfa, delta_alfa = anal.T
boner = anal.T
#print(boner[0]/boner[1])
#points=[boner[0]/boner[1]]
points = [(a/b) for (a,b) in filtered_list]
type(points)


klz_pocitadlo = True
klz = 0
for i, hodnota in enumerate(points):
	if len(points) -2 >=i and (abs(points[i]-points[i+1])/points[i]) <= 0.01:
		klz = 0
	else:
		klz = klz + 1
		if klz == 10 and klz_pocitadlo == True:
			klz_pocitadlo = False
			medza_klzu = sigma[i]
			young = points[:i]
			helper = i
			
	
#kreslenie scatter grafu z dat v liste points
data = np.array(graf_list)
x,y = data.T
plt.scatter(x,y,s=0.5)

#linearna regresia pre funkciu y = kx + q
xds=round(len(delta_alfa)/10)
xs = np.array(delta_alfa[:xds])
ys = np.array(sigma_alfa[:xds])


#funkcia ktora vrati koeficienty k, q pre linearnu regresiu
def fitovanie_smernica_a_intercept(xs,ys):
	k = (((mean(xs) * mean(ys)) - mean(xs*ys)) / ((mean(xs)**2) - mean(xs**2)))
	q = mean(ys) - k*mean(xs)
	return k,q

#definovanie premennych pre fitovanie
k,q = fitovanie_smernica_a_intercept(xs,ys)
epsilon_skusane = np.array(delta_alfa)
sigma_skusane = np.array(sigma_alfa)

#najde sigma linearne tzn. vynasobi kazdu nameranu deformaciu nasim modulom pruznosti ziskanym z linearnej regresie
def sigma_lin(lin_list):
	lin_list = (lin_list*k)-95
	return lin_list
	
#pre kazdu nameranu hodnotu napatia pripocita nejaku konstantu
def sigma_exp(skus_list):
	skus_list = skus_list
	return skus_list

K = [epsilon_skusane]
K = sigma_lin(epsilon_skusane)
L = [sigma_skusane]
L = sigma_exp(sigma_skusane)


#pomocou boolean array porovna arrays K a L a v arrayi L najde prvu hodnotu K > L
#co je medza klzu
print('\n-----------------\n 1. Medza Klzu(Porovnavacia) = ',L[K > L][0],'\n-----------------\n')

#druhy sposob najdenia medze klzu...podla vzorca ε(plasticke) = ε[celkove(to je nase namerane)] - Sigma(namerane)/E(nase vypocitane) co musi byt >= ako 0.2% z ε(celkoveho)
def sigma_young(sigma_vydelene):
	sigma_vydelene = sigma_vydelene/k
	return sigma_vydelene

M = [sigma_skusane]	
M = sigma_young(sigma_skusane)

def epsilon_minus_sigma_young(epsi_pl):
	epsi_pl = epsi_pl - M
	return epsi_pl

vysledok = epsilon_minus_sigma_young(epsilon_skusane)
print('\n-----------------\n 2. Medza Klzu(Norma) = ',sigma_alfa[vysledok > (epsilon_skusane*0.3)][0],'\n-----------------\n')

#koeficienty regresie
print('k = ', k/100000, 'q = ', q)
krivka_regresie = [(k*x)+q for x in xs]

#modul pruznosti z povodnej metody
try:
	print('\n---------------------------------\n Modul pruznosti 1(percentual) :',round((((sum(young))/helper)/100000),3),'\n---------------------------------\n')
except NameError:
	pass

#modul pruznosti z regresie
print('\n---------------------------------\n Modul pruznosti 2(regresia) :',round(k/100000,3),'\n---------------------------------\n')

#trvanie vsetkych vypoctov programu
t2=time.time()
print(t2-t1,'[s]---- trvanie\n')


#toto fituje krivku k bodom.
fit=np.polyfit(x,y,15)
p=np.poly1d(fit)
p.order
plt.title('Ťahový diagram')
plt.xlabel('deformacia')
plt.ylabel('napatie')
plt.plot(xs, krivka_regresie,"r--")
plt.show()