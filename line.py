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
		#sigma = list(filter(lambda x: x >= 0, sigma_alfa))
		#delta = list(filter(lambda x: x>0, delta_alfa))
		points = [float(b) / float(m) for b, m in zip(sigma_alfa, delta_alfa)]
		#if delta == 0:
		#	print('Error: Division by zero\nStlpce vo vstupnom subore su pravdepodobne vymenene.')
		#	sys.exit(0)
		#else:
		#	points = [float(b) / float(m) for b, m in zip(sigma, delta)]
			



n=len(points)
delenec = int(round(n/10))

klz_pocitadlo = True
klz = 0
#tato funkcia najde youngov modul pruznosti pre kazdy point a porovna ho s nasledujucim 
for i, vydelene in enumerate(points):
	if vydelene==0:
		print("0")
	else:
		if i>=len(points)-delenec:
			print("end")
		else:
			if(abs(vydelene-points[i+delenec]))/vydelene <= 0.1:
				#print(vydelene,"\t",i/100000,"\t\t",(abs(i-points[vydelene+delenec]))/i,"\t",'\t\tsedi\n')
				klz = 0
			else:
				#print(vydelene,"\t",i/100000,"\t\t",(abs(i-points[vydelene+delenec]))/i,'\t','\t\tnesedi\n')
				klz = klz + 1
				if klz == 10 and klz_pocitadlo == True:
					klz_pocitadlo = False
					medza_klzu = sigma_alfa[i]
					young = points[0:i]
					helper = i
t2=time.time()

print(points[0],'----prva hodnota points\n')
print(t2-t1,'[s]---- trvanie\n')

#print(min(sigma, key=float),'\n')
#print(min(delta, key=float),'\n')
print(min(delta_alfa, key=float),'----minimalna deformacia\n')
print(min(sigma_alfa, key=float),'----minimalne napatie\n')
print(len(points),"Pocet hodnot.")
print(helper,"Index hodnoty medzy klzu.")
print('\n---------------------------------\n Modul pruznosti :',round((((sum(young))/helper)/100000),3),'\n---------------------------------\n')
#najde medzu pevnosti a maximalne predlzenie
print('\n*Taznost je iba informativna*\n---------------------------------\n Taznost je :',(round(max(delta_alfa,key=float),3))*100,'%\n---------------------------------\n')
print('\n---------------------------------\n Medza pevnosti :', round(max(sigma_alfa,key=float),3),'MPa \n---------------------------------\n')
#print('\n---------------------------------\n Maximalna deformacia: ', round(max(delta,key=float),3),'\n---------------------------------\n')
print('\n---------------------------------\n Medza klzu :', round(medza_klzu,3),'MPa\n---------------------------------\n')

#deklaruje premennu data v ktorej su hodnoty z points zoradene do radu
data = np.array(graf_list)
#transponuje maticu data
x,y = data.T
#kresli scatter graf z matice data
plt.scatter(x,y,s=0.5)
#print(data)

#toto fituje krivku k bodom.
fit=np.polyfit(x,y,15)
p=np.poly1d(fit)
p.order
plt.title('Ťahový diagram')
plt.xlabel('deformacia')
plt.ylabel('napatie')
plt.plot(x,p(x),"r--")
plt.show()




