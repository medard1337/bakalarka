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

#predikcny interval
#1
x1 = np.array(lognf_1)
y1 = np.array(logsa_1)
X1 = sm.add_constant(x1)
#2
x2 = np.array(lognf_2)
y2 = np.array(logeap_2)
X2 = sm.add_constant(x2)
#3
x3 = np.array(logsa_3)
y3 = np.array(logeap_3)
X3 = sm.add_constant(x3)

#Fit the model
def re(y, X):
	re = sm.OLS(y, X).fit()
	return re
re1=re(y1,X1)
re2=re(y2,X2)
re3=re(y3,X3)
#1
#re1 = sm.OLS(y1, X1).fit()
#st, data, ss2 = summary_table(re1, alpha=0.05)
#print(data)
#2
#re2 = sm.OLS(y2, X2).fit()
#3
#re3 = sm.OLS(y3, X3).fit()

def d(re):
	st, data, ss2 = summary_table(re, alpha=0.05)
	return st, data, ss2
#st, data, ss2 = summary_table(re, alpha=0.01)
d(re1)
print(data)

da2=d1(re2)
da3=d1(re2)
#Get the confidence intervals
fittedvalues = data[:,2]
predict_mean_se  = data[:,3]
predict_mean_ci_low, predict_mean_ci_upp = data[:,4:6].T
predict_ci_low, predict_ci_upp = data[:,6:8].T




#deklaruje prazdny figure
fig = plt.figure()

graf4 = fig.add_subplot(811)
plt.scatter(lognf_1, logsa_1, s=0.9)
plt.title('WK')
plt.ylabel(r'Log $\sigma_a$')
plt.xlabel(r'Log 2N$\_f$')
plt.plot(xs1r,krivkaregresie_WK,"r-")

graf5 = fig.add_subplot(813)
plt.scatter(lognf_2, logeap_2, s=0.9)
plt.title('MCK')
plt.ylabel(r'Log $\epsilon_ap$')
plt.xlabel('Log 2Nf')
plt.plot(xs2r,krivkaregresie_MCK,"r-")

graf6 = fig.add_subplot(815)
plt.scatter(logsa_3, logeap_3, s=0.9)
plt.title('CDK')
plt.xlabel(r'Log $\sigma_a$')
plt.ylabel(r'Log $\epsilon_ap$')
plt.plot(xs3, krivkaregresie_CDK,"r-")

##############################################
#Plot confidence intervals and data points
graf6 = fig.add_subplot(816)
plt.plot(x1, y1, 'o')
plt.plot(x1, fittedvalues, '-', lw=1)
plt.plot(x1, predict_ci_low, 'r--', lw=1)
plt.plot(x1, predict_ci_upp, 'r--', lw=1)
plt.plot(x1, predict_mean_ci_low, 'g--', lw=1)
plt.plot(x1, predict_mean_ci_upp, 'g--', lw=1)


plt.subplots_adjust(hspace=0.01)
plt.show()






