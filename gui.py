from Tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def show_entry_fields():
	print("Zadal si filename %r" % (e1.get()))
def vykresli():
	csv = pd.read_csv(e1)
	data=csv[['deformacia','napatie']]
	data=data.astype(float)
	x=data['deformacia']
	y=data['napatie']
	plt.scatter(x,y,s=0.5)
	#toto fituje krivku k bodom.
	fit=np.polyfit(x,y,15)
	p=np.poly1d(fit)
	plt.plot(x,p(x),"r--")
	plt.show()


master = Tk()
master.minsize(width=666, height=666)
Label(master, text="Filename").grid(row=0)

e1 = Entry(master)
e1.grid(row=0, column=1)

Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='Show', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)
Button(master, text='Kresli', command=vykresli).grid(row=3, column=2, sticky=W,pady=4)

mainloop( )