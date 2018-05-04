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
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from statsmodels.stats.outliers_influence import summary_table


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

print('\n(WK) Koeficient b =', b_WK,'Koeficient Sigmaf = ',sigmaf_WK)
print('\n(MCK) Koeficient b =', b_MCK,'Koeficient Sigmaf =',sigmaf_MCK)
print('\n(CDK) Koeficient b =', b_CDK,'Koeficient Sigmaf =',sigmaf_CDK)

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


#konfidencny interval
#def mean_confidence_interval(data, confidence=0.95):
#	a = 1.0*np.array(data)
#	n = len(a)
#	m, se =np.mean(a), scipy.stats.sem(a)
#	h = se * scipy.stats.t._ppf((1+confidence)/2.,n-1)
#	return m, m-h, m+h

#print('\nKonfidencny interval WK: ',mean_confidence_interval(krivkaregresie_WK))
#print('\nKonfidencny interval MCK: ',mean_confidence_interval(krivkaregresie_MCK))
#print('\nKonfidencny interval CDK: ',mean_confidence_interval(krivkaregresie_CDK))


############################################################################
#predikcny interval
#1
x1_0 = np.array(lognf_1)
y1_0 = np.array(logsa_1)
combo1 = np.vstack((x1_0,y1_0)).T
sort1=np.array(sorted(combo1, key=lambda l: l[1]))
x1, y1 = sort1.T
X1 = sm.add_constant(x1)
#2
x2_0 = np.array(lognf_2)
y2_0 = np.array(logeap_2)
combo2 = np.vstack((x2_0,y2_0)).T
sort2=np.array(sorted(combo2, key=lambda l: l[1]))
x2, y2 = sort2.T
X2 = sm.add_constant(x2)
#3
x3_0 = np.array(logsa_3)
y3_0 = np.array(logeap_3)
combo3 = np.vstack((x3_0,y3_0)).T
sort3=np.array(sorted(combo3, key=lambda l: l[1]))
x3, y3 = sort3.T
X3 = sm.add_constant(x3)







#Fit the model
def re(y, X):
	re = sm.OLS(y, X).fit()
	return re
re1=re(y1,X1)
re2=re(y2,X2)
re3=re(y3,X3)

def d(re,alpha):
	st, data, ss2 = summary_table(re, alpha)
	return st,data,ss2


#99%
da1_99=d(re1,0.01)[1]
da2_99=d(re2,0.01)[1]
da3_99=d(re3,0.01)[1]


#95% intervaly
da1_95=d(re1,0.05)[1]
da2_95=d(re2,0.05)[1]
da3_95=d(re3,0.05)[1]

#50%
da1_50=d(re1,0.5)[1]
da2_50=d(re2,0.5)[1]
da3_50=d(re3,0.5)[1]

#Get the confidence intervals
def conf_interval(da):
	fittedvalues = da[:,2]
	predict_mean_se  = da[:,3]
	predict_mean_ci_low, predict_mean_ci_upp = da[:,4:6].T
	predict_ci_low, predict_ci_upp = da[:,6:8].T
	return fittedvalues, predict_mean_se,predict_mean_ci_low,predict_mean_ci_upp,predict_ci_low,predict_ci_upp


#conf intervaly
#99%
c1_99=conf_interval(da1_99)
c2_99=conf_interval(da2_99)
c3_99=conf_interval(da3_99)

#95%
c1_95=conf_interval(da1_95)
c2_95=conf_interval(da2_95)
c3_95=conf_interval(da3_95)

#50%
c1_50=conf_interval(da1_50)
c2_50=conf_interval(da2_50)
c3_50=conf_interval(da3_50)
######################################################################################################################################


#deklaruje prazdny figure
fig = plt.figure()

#Plot confidence intervals and data points

def graf(x,y,c):
	plt.plot(x, y, '.',label='Vstupné dáta')
	plt.plot(x, c[0], '-', lw=1,label='Regresná krivka')
	plt.plot(x, c[4], 'r--', lw=1, label='Predikčný interval')
	plt.plot(x, c[5], 'r--', lw=1, label='Predikčný interval')
	plt.plot(x, c[2], 'g--', lw=1, label='Konfidenčný interval')
	plt.plot(x, c[3], 'g--', lw=1, label='Konfidenčný interval')


#WK 99%
graf1 = fig.add_subplot(331)
plt.title('WK 99%')
graf(x1,y1,c1_99)

#MCK99%
graf2 = fig.add_subplot(332)
plt.title('MCK 99%')
graf(x2,y2,c2_99)

#CDK99%
graf3 = fig.add_subplot(333)
plt.title('CDK 99%')
graf(x3,y3,c3_99)

#WK 95%
graf4 = fig.add_subplot(334)
plt.title('WK 95%')
graf(x1,y1,c1_95)

#MCK95%
graf5 = fig.add_subplot(335)
plt.title('MCK 95%')
graf(x2,y2,c2_95)

#CDK 95%
graf6 = fig.add_subplot(336)
plt.title('CDK 95%')
graf(x3,y3,c3_95)

#WK 50%
graf7 = fig.add_subplot(337)
plt.title('WK 50%')
graf(x1,y1,c1_50)

#MCK50%
graf8 = fig.add_subplot(338)
plt.title('MCK 50%')
graf(x2,y2,c2_50)

#CDK50%
graf9 = fig.add_subplot(339)
plt.title('CDK 50%')
graf(x3,y3,c3_50)



plt.legend(bbox_to_anchor=(1,1),loc=2, borderaxespad=0.)
plt.subplots_adjust(hspace=0.8)
plt.show()






