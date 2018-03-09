import pylab as pl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
		#pripise hodnoty napatia a deformacie do listu points
		points.append([deformacia,napatie])



#deklaruje premennu data v ktorej su hodnoty z points zoradene do radu
data = np.array(points)
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
#plt.plot(x,p(x),"r--")
plt.show()








