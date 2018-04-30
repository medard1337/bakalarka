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
logeap_3 = logeap_2


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
krivkaregresie_WK = [(k1*x)+q1 for x in xs1]

# #linearna regresia pre krivku MCK a tvar jej usecky
xs2,ys2 = points_for_lin_regression(logeap_2,lognf_2)
k2,q2 = fitovanie_slope_a_intercept(xs2,ys2)
krivkaregresie_MCK = [(k2*x)+q2 for x in xs2]

#linearna regresia pre krivku CDK a tvar jej krivky
xs3,ys3 = points_for_lin_regression(logsa_3,logeap_3)
k3,q3 = fitovanie_slope_a_intercept(xs3,ys3)
krivkaregresie_CDK = [(k3*x)+q3 for x in xs3]

print('\n','koef. pre WK:','\n--------------------------\n','k =',k1,'\n','q  =',q1)
print('\n','koef. pre WK:','\n--------------------------\n','k =',k2,'\n','q  =',q2)
print('\n','koef. pre WK:','\n--------------------------\n','k =',k3,'\n','q  =',q3)



#print('lognf_1',lognf_1)
#print('nf_1',nf_1)
#print('logsa_1',logsa_1)
#print('sa_1',sa_1)

#printuje listy, iba kontrolna vec
#print('\n\n',nf_1)
#print('\n\n\ngraf wk',final_list_WK)
#print('\n\ngraf mck',final_list_MCK)
#print('\n\ngraf cdk',final_list_CDK)

#deklaruje prazdny figure
fig = plt.figure()

#grafy z jednotlivych listov
graf1 = fig.add_subplot(611)

plt.scatter(nf_1,sa_1,s=0.5)
plt.title('qoqot')

graf2 = fig.add_subplot(612)

plt.scatter(nf_2, eap_2,s=0.5)
plt.title('vaginqa')

graf3 = fig.add_subplot(613)

plt.scatter(eap_3,sa_3,s=0.5)
plt.title('analiq')

graf4 = fig.add_subplot(614)
plt.scatter(logsa_1, lognf_1, s=0.9)
plt.title('WK')
plt.xlabel('Log Sa')
plt.ylabel('Log 2Nf')
plt.plot(xs1, krivkaregresie_WK,"r-")

graf5 = fig.add_subplot(615)
plt.scatter(logeap_2, lognf_2, s=0.9)
plt.title('MCK')
plt.xlabel('Log Eap')
plt.ylabel('Log 2Nf')
plt.plot(xs2, krivkaregresie_MCK,"r-")

graf6 = fig.add_subplot(616)
plt.scatter(logsa_3, logeap_3, s=0.9)
plt.title('CDK')
plt.xlabel('Log Sa')
plt.ylabel('Log Eap')
plt.plot(xs3, krivkaregresie_CDK,"r-")

plt.subplots_adjust(hspace=1.7)
plt.show()






