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
peror = []

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
			print('Zly vyber')
		
		
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
print('E = ', k, 'q = ', q)
krivka_regresie = [(k*x)+q for x in xs]
#r_squared = koeficient_determinantu(ys, krivka_regresie)
#print('r^2 = ', r_squared)

yd_sigma = round(len(sigma_alfa))
xd_epsilon = round(len(delta_alfa))
epsilon_skusane = np.array(delta_alfa[:xd_epsilon])
sigma_skusane = np.array(sigma_alfa[:yd_sigma])

#najde sigma linearne tzn. vynasobi kazdu nameranu deformaciu nasim modulom pruznosti
def sigma_lin(lin_list):
	lin_list = lin_list*k
	return lin_list
	
#pre kazdu nameranu hodnotu napatia pripocita nejaku konstantu
def sigma_exp(skus_list):
	skus_list = skus_list + 20
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
#H = sigma_vydelene

def epsilon_div_sigma_young(x):
	epsi_pl = ((x - cde)/0.002)
	return epsi_pl
	
vysledok = epsilon_div_sigma_young(epsilon_skusane)
efg = np.array([vysledok])
fgh = np.array([delta_alfa])
print('\n-----------------\n 2. Medza Klzu = ',(efg[efg >= fgh][0])*100000,'\n-----------------\n')


	
#N = epsilon_div_sigma_young(epsilon_skusane, sigma_vydelene)
#print(M)
#print('VYSLEDOK',vysledok)
#print('cde',cde)
	
#N = [epsilon_skusane]
#N = epsilon_div_sigma_young(epsilon_skusane)

#def function(x, H):
#	return x - H
	
#fun = function(epsilon_skusane)
	

#print(fun)

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
plt.plot(xs, krivka_regresie,"m--")
plt.show()



