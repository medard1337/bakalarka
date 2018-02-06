import csv




#filename=input('Enter fileame ')
rawfile=open('file.csv', 'r')
with open(rawfile,'rb') as l:
	reader = csv.reader(l)
	podiel = list(reader)


print(podiel)



podiel=[]

#for l in rawfile:
#	if len(l) > 0: