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

final_list = []
Nf_1 = []
Sa_1 = []
Nf_2 = []
Eap_2 = []
Eap_3 = []
Sa_3 = []
graf_list_CDK = []
graf_list_MCK = []
graf_list_WK = []

#premeni string na float
def tofloat(string):
	if (string):
		return float(string)
	return 0.0
	
#timer
t1 = time.time()

for l in rawfile:
	if 1 > 0 and not l.startswith(' " '):
		l.rstrip(" ")
		l.rstrip("\n ")
		l.rstrip(",")
		l.rstrip(" ")
		l.rstrip(";")
		split = l.split('\t')
		
		Nf1 = tofloat(split[0])
		Sa1 = tofloat(split[1])
		Nf2 = tofloat(split[2])
		Eap2 = tofloat(split[3])
		Eap3 = tofloat(split[4])
		Sa3 = tofloat(split[5])
		final_list.append([Nf1, Sa1, Nf2, Eap2, Eap3, Sa3])
			
		Nf_1.append(Nf1)
		Sa_1.append(Sa1)
		Nf_2.append(Nf2)
		Eap_2.append(Eap2)
		Eap_3.append(Eap3)
		Sa_3.append(Sa3)
		graf_list_WK.append([Nf1, Sa1])
		graf_list_MCK.append([Nf2, Eap2])
		graf_list_CDK.append([Eap3, Sa3])
		
print(graf_list_CDK)
			