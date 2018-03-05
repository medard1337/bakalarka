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
		if vydelene>=len(points)-1:
			print("end")
		else:
			if(abs(i-points[vydelene+1]))/i <= 0.03:
				print(vydelene,"\t",i/100000,"\t\t",(abs(i-points[vydelene+1]))/i,"\t",'\t\tsedi\n')
			else:
				print(vydelene,"\t",i/100000,"\t\t",(abs(i-points[vydelene+1]))/i,'\t','\t\tnesedi\n')

#najde medzu pevnosti a maximalne predlzenie	

print('*Taznost je iba informativna*\n---------------------------------\n Taznost je :',(round(max(delta,key=float),5))*100,'%\n---------------------------------\n')

print('\n---------------------------------\n Medza pevnosti =', round(max(sigma,key=float),5),'MPa \n---------------------------------\n')
print('\n---------------------------------\n Maximalna deformacia: ', round(max(delta,key=float),5),'\n---------------------------------\n')




#podiel_file=Path(filename).stem + "_linearita.csv"
#print(podiel_file)
#podiel_file.to_csv(podiel_file,index=False)
#with open(podiel_file, 'w') as output_file:
#	file_writer = csv.writer(output_file)
#	file_writer.writerows(points)