import pylab as pl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from pathlib import Path

#otvori subor
filename=input('Enter filename ')
rawfile = open(filename, 'r')
#deklaruje prazdny list s nazvom points
points = []


#tato funkcia premiena string na float
def tofloat(string):
    if (string):
        return float(string)
    return 0.0


	

#tato funkcia prechadza input subor riadok po riadku
for l in rawfile:
	#ak je v riadku viac ako 0 znakov a nezacina sa "
	if len(l) > 0 and not l.startswith('"'):
		#odstrani \n -> symboly noveho riadku
		l.rstrip("\n ")
		l.rstrip(",")
		l.rstrip(" ")
		#rozdeli hodnoty tam kde su rozdelene tabulatorom
		split = l.split('\t')
		#premeni hodnoty v prvom stlci na float a nazve ich napatie
		napatie = tofloat(split[0])
		#premeni hodnoty v druhom stlpci na float a nazve ich deformacia
		deformacia = tofloat(split[1])
		podiel = napatie/deformacia
		#pripise hodnoty napatia a deformacie do listu points
		points.append([podiel])

##########################################
#def remove_negs(linearita):
#	for item in linearita:
#		if item < 0:
#			linearita.remove(item)
##########################################


podiel_file=Path(filename).stem + "_linearita.csv"
print(podiel_file)
with open(podiel_file, 'w') as output_file:
	file_writer = csv.writer(output_file)
	file_writer.writerows(points)