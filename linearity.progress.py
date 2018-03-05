import pylab as pl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from pathlib import Path
from math import ceil
import decimal

#otvori subor
filename=input('Enter filename ')
pocdlzka=float(input("Zadaj povodnu dlzku meranej vzorky: "))
rawfile = open(filename, 'r')
#deklaruje prazdny list s nazvom points
points = []
vydelene = []
sigma = []
delta = []
gama = []

#tato funkcia premiena string na float
def tofloat(string):
    if (string):
        return float(string)

    return 0.0

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
		#premeni hodnoty v prvom stlci na float a nazve ich napatie
		napatie = tofloat(split[0])
		#premeni hodnoty v druhom stlpci na float a nazve ich deformacia
		deformacia = tofloat(split[1])
		#pripise hodnoty napatia a deformacie do listu points
		sigma.append(napatie)
		delta.append(deformacia)
		points.append(napatie/deformacia)

#tato funkcia najde youngov modul pruznosti pre kazdy point a porovna ho s nasledujucim 
for vydelene, i in enumerate(points):
	if i==0:
		print("0")
	else:
		if vydelene>=len(points)-4:
			print("end")
		else:
			if(abs(i-points[vydelene+4]))/i <= 0.03:
				print(vydelene,"\t",i/100000,"\t\t",(abs(i-points[vydelene+4]))/i,"\t",'\t\tsedi\n')
			else:
				print(vydelene,"\t",i/100000,"\t\t",(abs(i-points[vydelene+4]))/i,'\t','\t\tnesedi\n')

#najde medzu pevnosti a maximalne predlzenie	
print('\n------------------------------\n Medza pevnosti =', max(sigma,key=float),'MPa \n------------------------------\n')
print('*Taznost je iba informativna*\n------------------------------\n Taznost je :', ceil(((((pocdlzka + abs(max(delta, key=float))) - pocdlzka) * 100) / pocdlzka) * 100) / 100.0, '%')

#pocdlzka=float(input("Zadaj povodnu dlzku meranej vzorky: "))
#taznost= ((('max_in_list(deformacia)') - pocdlzka) * 100)/pocdlzka
#print('Taznost je :', taznost)
	

#taznost=(((max_in_list(deformacia)-pocdlzka)/pocdlzka)*100)
#print('Taznost =', taznost, '%')
#def max_in_napatie(napatie):
#	maxVal=napatie[0]
##		if i>maxVal:
#			maxVal = i
##	return maxVal
#print(max(napatie, key=float))
#print(max_in_napatie(napatie))
				
#from itertools import groupby

#srt_list = sorted(napatie, key=lambda x: x[1]);

#max_list = []
#upby(srt_list, lambda x: x[1].split('.')[0]):
	#max_el = max(list(group), key = lambda y: int(y[1].split('.')[1]))
	#max_list.append(float(max_el[1]))
				
#for x in points:
#	if x == 0 in points:
#		print('0')
#	else:
#		vydelene.append((x+1)/x)



#print("------------------------------------------")
#for j in vydelene:
	#print(abs((j)-(j+1))/j)
	#print(j)
	#print(j+1)

	
#for u in vydelene:
#	if abs((u)-(u+1))/u >= 0.99999:
#		print("Vaginka")
#	else:
#		print("analik")

	
##########################################
#def remove_negs(linearita):
#	for item in linearita:
#		if item < 0:
#			linearita.remove(item)
##########################################


#podiel_file=Path(filename).stem + "_linearita.csv"
#print(podiel_file)
#podiel_file.to_csv(podiel_file,index=False)
#with open(podiel_file, 'w') as output_file:
#	file_writer = csv.writer(output_file)
#	file_writer.writerows(points)