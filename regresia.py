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
		if deformacia == 0:
			print('Error: Division by zero\nStlpce vo vstupnom subore su pravdepodobne vymenene.')
			sys.exit(0)
		else:
			points.append(napatie/deformacia)

#transponovanie matice filtered_list
anal = np.array(filtered_list)
sigma_alfa, delta_alfa = anal.T

#deklaruje premennu data v ktorej su hodnoty z points zoradene do radu
data = np.array(graf_list)
#transponuje maticu data
x,y = data.T
#kresli scatter graf z matice data
plt.scatter(x,y,s=0.5)

#linearna regresia pre funkciu y = kx + q
xds=round(len(delta_alfa)/10)
xs = np.array(delta_alfa[:xds])
ys = np.array(sigma_alfa[:xds])


klz_pocitadlo = True
klz = 0
#tento cyklus rata modul pruznosti z kazdej dvojice [napatie, deformacia] a porovna ci sa lisi o 5% od nasledujuceho
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



#funkcia ktora vrati koeficienty k, q pre linearnu regresiu
def fitovanie_smernica_a_intercept(xs,ys):
	k = (((mean(xs) * mean(ys)) - mean(xs*ys)) / ((mean(xs)**2) - mean(xs**2)))
	q = mean(ys) - k*mean(xs)
	return k,q

#definovanie premennych pre fitovanie
k,q = fitovanie_smernica_a_intercept(xs,ys)
yd_sigma = round(len(sigma_alfa))
xd_epsilon = round(len(delta_alfa))
epsilon_skusane = np.array(delta_alfa[:xd_epsilon])
sigma_skusane = np.array(sigma_alfa[:yd_sigma])

#najde sigma linearne tzn. vynasobi kazdu nameranu deformaciu nasim modulom pruznosti ziskanym z linearnej regresie
def sigma_lin(lin_list):
	lin_list = lin_list*k
	return lin_list
	
#pre kazdu nameranu hodnotu napatia pripocita nejaku konstantu
def sigma_exp(skus_list):
	skus_list = skus_list + 15
	return skus_list

K = [epsilon_skusane]
K = sigma_lin(epsilon_skusane)
L = [sigma_skusane]
L = sigma_exp(sigma_skusane)

#vytvori z hodnot K a L arrays a potom ich pomocou boolean array porovna a najde prvu hodnotu v array K ktora odpoveda indexu  v array L a je vacsia,
#co je medza klzu
abc = np.array([K])
bcd = np.array([L])
print('\n-----------------\n 1. Medza Klzu = ',abc[abc > bcd][0],'\n-----------------\n')


#druhy sposob najdenia medze klzu...podla vzorca ε(plasticke) = ε[celkove(to je nase namerane)] - Sigma(namerane)/E(nase vypocitane) co musi byt >= ako 0.2% z ε(celkoveho)
def sigma_young(sigma_vydelene):
	sigma_vydelene = sigma_vydelene/k
	return sigma_vydelene

M = [sigma_skusane]	
M = sigma_young(sigma_skusane)
cde = np.array([M])


def epsilon_div_sigma_young(x):
	epsi_pl = ((x - cde)/0.002)
	return epsi_pl

vysledok = epsilon_div_sigma_young(epsilon_skusane)
efg = np.array([vysledok])
fgh = np.array([delta_alfa])
print('\n-----------------\n 2. Medza Klzu = ',(efg[efg >= fgh][0])*100000,'\n-----------------\n')

try:
	regres2=(sum(young)/helper)
except NameError:
	pass
print('E = ', k/100000, 'q = ', q)
krivka_regresie = [(k*x)+q for x in xs]

#modul pruznosti z povodnej metody
try:
	print('\n---------------------------------\n Modul pruznosti 1 :',round((((sum(young))/helper)/100000),3),'\n---------------------------------\n')
except NameError:
	pass

#modul pruznosti z regresie
print('\n---------------------------------\n Modul pruznosti 2 :',round(k/100000,3),'\n---------------------------------\n')

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