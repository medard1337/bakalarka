# -*- coding: utf-8 -*-
from Tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


master=Tk()

class App:

	def __init__(self, master):
		master.minsize(width=666, height=666)
        
		frame = Frame(master)
		frame.pack()

		self.button = Button(frame, text="Vyziadaj filename", fg="red", command=udaj)
		self.button.pack(side=LEFT)
		self.hi_there = Button(frame, text="Vykresli", command=self.vykresli)
		self.hi_there.pack(side=LEFT)
	#	L1=Label(master, text="Enter filename faggot: ")
	#	E1=Entry(master)
	#	E1.pack(side=LEFT)
	#	enterbutton=Button(master,test="Submit",command=E1.get())
	#	enterbutton.pack(side=BOTTOM)

	def udaj():
		L1=Label(master, text="Enter filename, faggot")
		L1.pack(side=LEFT)
		global E1
		E1=Entry(master)
		E1.pack(side=RIGHT)
		enterbutton=Button(master, text="Submit",command=E1.get())
		enterbutton.pack(side=BOTTOM)
		master.mainloop()
	def vykresli():
		csv = pd.read_csv(E1)
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





if __name__=="__main__":

    root = Tk()
    app = App(root)
    root.mainloop()