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
import math

filename = input('Enter filename ')
rawfile = open(filename, 'r')
rawfile.readline()
rawfile.readline()

final_list_WK = []
final_list_MCK = []
final_list_CDK = []
analnik=[]

def tofloat(string):
	if (string.strip()):
		#print(string)
		return float(string.replace(",","."))
	return 0.0

#splituje datovy subor a parsuje ho do listov
for l in rawfile:
	if not l.startswith('"'):
		split_l = l.split(';')
		Nf1 = tofloat(split_l[0])
		Sa1 = tofloat(split_l[1])
		analnik.append([Nf1])
		if (Nf1 > 0 and Sa1 > 0):
			final_list_WK.append([Nf1, Sa1])
		Nf2 = tofloat(split_l[2])
		Eap2 = tofloat(split_l[3])
		if (Nf2 > 0 and Eap2 > 0):
			final_list_MCK.append([Nf2, Eap2])
		Eap3 = tofloat(split_l[4])
		Sa3 = tofloat(split_l[5])
		if (Eap3 > 0 and Sa3 > 0):
			final_list_CDK.append([Eap3, Sa3])

wklist = np.array(final_list_WK)
nf_1, sa_1 = wklist.T
mcklist = np.array(final_list_MCK)
nf_2, eap_2 = mcklist.T
cdklist = np.array(final_list_CDK)
eap_3, sa_3 = cdklist.T

#zlogaritmovane vsetky arraye podla toho ako su vykreslovane, tzn v krivka WK - 2Nf voci Sa,  MCK - 2Nf voci Eap, CDK - Sa voci Eap
#2Nf je dvojnasobok poctu cyklov, Eap je deformacia ktora vznikla na meranej vzorke, Sa je sigma a - napatie
#2Nf musim logaritmovat aj pre WK aj MCK pretoze maju rozlisne rozmery ale, ale Eap staci logaritmovat iba raz pretoze aj MCK aj CDK 
#maju rovnake rozmery, Sa musim taktie logaritmovat 2 krat, raz pre WK a raz pre CDK
lognf_1 = [math.log(x) for x in nf_1]
logsa_1 = [math.log(x) for x in sa_1]
lognf_2 = [math.log(x) for x in nf_2]
logeap_2 = [math.log(x) for x in eap_2]
logsa_3 = [math.log(x) for x in sa_3]
logeap_3 = [math.log(x) for x in eap_3]


#pomocou tejto funkcie zvolime body pre danu linearnu regresiu a vypluje nam to upravene x a y body
def points_for_lin_regression(log_x_axis,log_y_axis):
	xs = np.array(log_x_axis)
	ys = np.array(log_y_axis)
	return xs,ys
	
#funkcia z ktorej dostaneme koeficienty krivky linearnej regresie pre dany graf	
def fitovanie_slope_a_intercept(xs,ys):
	k = (((mean(xs) * mean(ys)) - mean(xs*ys)) / ((mean(xs)**2) - mean(xs**2)))
	q = mean(ys) - k*mean(xs)
	return k,q

#linearna regresia pre krivku WK	a tvar jej usecky
xs1,ys1 = points_for_lin_regression(logsa_1,lognf_1)
k1,q1 = fitovanie_slope_a_intercept(xs1,ys1)

# #linearna regresia pre krivku MCK a tvar jej usecky
xs2,ys2 = points_for_lin_regression(logeap_2,lognf_2)
k2,q2 = fitovanie_slope_a_intercept(xs2,ys2)

#linearna regresia pre krivku CDK a tvar jej krivky
xs3,ys3 = points_for_lin_regression(logsa_3,logeap_3)
k3,q3 = fitovanie_slope_a_intercept(xs3,ys3)
krivkaregresie_CDK = [(k3*x)+q3 for x in xs3]

def new_koeficient_b_Sigmaf(x,q):
	b = 1/x
	sigmaf = 1/(math.exp(q*b))
	return b,sigmaf
	
#koeficienty b a Sigmaf pre krivku WK:
b_WK,sigmaf_WK = new_koeficient_b_Sigmaf(k1,1/k1)
novakrivkaregresie_WK = [sigmaf_WK*(nf_1)**b_WK]

#koeficient b a sigmaf pre krivku MCK
b_MCK,sigmaf_MCK = new_koeficient_b_Sigmaf(k2,1/k2)
novakrivkaregresie_MCK = [sigmaf_MCK*(nf_2)**b_MCK]

#koeficient b a sigmaf pre kticku CDK
b_CDK,sigmaf_CDK = new_koeficient_b_Sigmaf(k3,1/k3)
#vytvorena nova krivka pre povodne grafy tzn Sigma a voci 2Nf
#novakrivkaregresie_CDK = [sigmaf_CDK*(nf_1)**b_CDK]

print('(WK) Koeficient b =', b_WK,'Koeficient Sigmaf = ',sigmaf_WK)
print('(MCK) Koeficient b =', b_MCK,'Koeficient Sigmaf =',sigmaf_MCK)
print('(CDK) Koeficient b =', b_CDK,'Koeficient Sigmaf =',sigmaf_CDK)

#linearna regresia pre reverznute osi tzn. na osi x-ovej je 2Nf aj v pripade krivky WK aj MCK , na krivke WK je na osi y Sigma a
#a na krivke MCK je na osi y Epsilon ab
#reverznuta WK
xs1r,ys1r = points_for_lin_regression(lognf_1,logsa_1)
k1r,q1r = fitovanie_slope_a_intercept(xs1r,ys1r)
krivkaregresie_WK = [(k1r*x)+q1r for x in xs1r]

#reverznuta MCK
xs2r,ys2r = points_for_lin_regression(lognf_2,logeap_2)
k2r,q2r = fitovanie_slope_a_intercept(xs2r,ys2r)
krivkaregresie_MCK = [(k2r*x)+q2r for x in xs2r]

def sigma_a(sigmaf,Nf,b):
	sigmaa = sigmaf*(Nf)**b
	return sigmaa
	
sigmaaWK = sigma_a(sigmaf_WK,nf_1,b_WK)
sigmaaMCK = sigma_a(sigmaf_MCK,nf_2,b_MCK)

#deklaruje prazdny figure
fig = plt.figure()

graf4 = fig.add_subplot(511)
plt.scatter(lognf_1, logsa_1, s=0.9)
plt.title('WK')
plt.ylabel(r'Log $\sigma_a$')
plt.xlabel(r'Log 2N$\_f$')
plt.plot(xs1r,krivkaregresie_WK,"r-")

graf5 = fig.add_subplot(513)
plt.scatter(lognf_2, logeap_2, s=0.9)
plt.title('MCK')
plt.ylabel(r'Log $\epsilon_ap$')
plt.xlabel('Log 2Nf')
plt.plot(xs2r,krivkaregresie_MCK,"r-")

graf6 = fig.add_subplot(515)
plt.scatter(logsa_3, logeap_3, s=0.9)
plt.title('CDK')
plt.xlabel(r'Log $\sigma_a$')
plt.ylabel(r'Log $\epsilon_ap$')
plt.plot(xs3, krivkaregresie_CDK,"r-")

plt.subplots_adjust(hspace=0.05)
plt.show()






