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


for l in rawfile:
  if not l.startswith('"'):
  
    split_l = l.split(';');
  
    Nf1 = tofloat(split_l[0]);
    Sa1 = tofloat(split_l[1]);
    final_list_WK.append([Nf1, Sa1]);
	
    Nf2 = tofloat(split_l[2]);
    Eap2 = tofloat(split_l[3]);
    final_list_MCK.append([Nf2, Eap2]);
	
    Eap3 = tofloat(split_l[4]);
    Sa3 = tofloat(split_l[5]);
    final_list_CDK.append([Eap3, Sa3]);
  
print('graf wk',final_list_WK)
print('graf mck',final_list_MCK)
print('graf cdk',final_list_CDK)