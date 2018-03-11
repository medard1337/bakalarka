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

#otvori subor
filename=input('Enter filename ')
rawfile = open(filename, 'r')
#deklaruje prazdny list s nazvom points
points = []
vydelene = []
sigma = []
delta = []


#tato funkcia premiena string na float
def tofloat(string):
	if (string):
		return float(string)
	return 0.0

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
			print('Zly vyber kokot')
		#premeni hodnoty v prvom stlci na float a nazve ich napatie
#		napatie = tofloat(split[0])
		#premeni hodnoty v druhom stlpci na float a nazve ich deformacia
#		deformacia = tofloat(split[1])
		#pripise hodnoty napatia a deformacie do listu points
		sigma.append(napatie)
		delta.append(deformacia)
		if deformacia == 0:
			print('Error: Division by zero\nStlpce vo vstupnom subore su pravdepodobne vymenene.')
			sys.exit(0)
		else:
			points.append(napatie/deformacia)

n = len(points)
deleec = n/100
klz_pocitadlo = True
klz = 0
#tato funkcia najde youngov modul pruznosti pre kazdy point a porovna ho s nasledujucim 
for i, vydelene in enumerate(points):
	if vydelene ==0:
		print("0")
	else:
		if i>=len(points)-40:
			print("end")
		else:
			if(abs(vydelene-points[i+40]))/vydelene <= 0.005:
				print(i,"\t",vydelene/100000,"\t\t",(abs(vydelene-points[i+40]))/vydelene,"\t",'\t\tsedi\n')
				klz = 0
			else:
				print(i,"\t",vydelene/100000,"\t\t",(abs(vydelene-points[i+40]))/vydelene,'\t','\t\tnesedi\n')
				klz = klz + 1
				if klz == 10 and klz_pocitadlo == True:
					klz_pocitadlo = False
					medza_klzu = sigma[i]
					young = points[0:i]
					helper = i
					print(max(points, key=float)/100000)

print(points[0],'\n')
print(len(points))
print(helper)
print(sum(young))					
print('\n---------------------------------\n Modul pruznosti :',round((((sum(young))/helper)/100000),3),'\n---------------------------------\n')
#najde medzu pevnosti a maximalne predlzenie
print('\n*Taznost je iba informativna*\n---------------------------------\n Taznost je :',(round(max(delta,key=float),3))*100,'%\n---------------------------------\n')
print('\n---------------------------------\n Medza pevnosti :', round(max(sigma,key=float),3),'MPa \n---------------------------------\n')
#print('\n---------------------------------\n Maximalna deformacia: ', round(max(delta,key=float),3),'\n---------------------------------\n')
print('\n---------------------------------\n Medza klzu :', round(medza_klzu,3),'MPa\n---------------------------------\n')


