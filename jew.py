d={
'part1':[
	'Gold',
	'Wasser',
	'Edel',
	'Bergen',
	'Braun',
	'Katzen',
	'Baren',
	'Apple',
	'Blumen',
	'Kronen',
	'Feigen',
	'Feld',
	'Green',
	'Hoch',
	'Rosen',
	'Silver',
	'Wein',
	'Zimmer'],
'part2':[
	'berg',
	'stein',
	'meyer',
	'owsky',
	'heimer',
	'baum',
	'feld',
	'bach',
	'witz',
	'mann',
	'span',
	'hirsch',
	'stern',
	'berger',],
}

import pickle
f=open('syllables','w')
pickle.dump(d,f)
f.close()

f1=open('syllables','r')
sd=pickle.load(f1)
f1.close()

import random
def gen():
	first_part=sd['part1'][random.randint(0,len(sd['part1'])-1)]
	second_part=sd['part2'][random.randint(0,len(sd['part2'])-1)]
	print ('%s%s')%(first_part,second_part)

n =str(raw_input("Reroll Y/N?"))
#while n == "Y":
	#gen
	#else 
#		break




