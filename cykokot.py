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

filename = input('Enter filename ')
rawfile = open(filename, 'r')
rawfile.readline()
rawfile.readline()

final_list_WK = []
final_list_MCK = []
final_list_CDK = []


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

#printuje listy, iba kontrolna vec
print('\n\ngraf wk',final_list_WK)
print('\n\ngraf mck',final_list_MCK)
print('\n\ngraf cdk',final_list_CDK)

#deklaruje prazdny figure
fig = plt.figure()

#grafy z jednotlivych listov
graf1 = fig.add_subplot(311)
wklist = np.array(final_list_WK)
nf_1, sa_1 = wklist.T
plt.scatter(nf_1,sa_1,s=0.5)
plt.title('qoqot')

graf2 = fig.add_subplot(312)
mcklist = np.array(final_list_MCK)
nf_2, eap_2 = mcklist.T
plt.scatter(nf_2, eap_2,s=0.5)
plt.title('vaginqa')

graf3 = fig.add_subplot(313)
cdklist = np.array(final_list_CDK)
eap_3, sa_3 = cdklist.T
plt.scatter(eap_3,sa_3,s=0.5)
plt.title('analiq')

plt.subplots_adjust(hspace=0.8)
plt.show()


