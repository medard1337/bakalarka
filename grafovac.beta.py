#tento skrip vykresluje scatter grafy z .CSV suborov.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



#toto si vypyta nazov aj s priponou a vykresli hodnoty z tabulky na scatter graf
filename=input('Enter filename ')
csv = pd.read_csv(filename)
data=csv[['deformacia','napatie']]
data=data.astype(float)
x=data['deformacia']
y=data['napatie']
plt.scatter(x,y,s=1)

#toto fituje krivku k bodom.
#fit=np.polyfit(x,y,15)
#p=np.poly1d(fit)
#plt.plot(x,p(x),"r--")
plt.show()



