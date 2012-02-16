#!/usr/bin/python

import sys

pileup=sys.argv[1]
codons=sys.argv[2]

#AAs  = FFLLSSSSYY**CCWWLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
#Starts = --MM---------------M------------MMMM---------------M------------
#Base1  = TTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGG
#Base2  = TTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGG
#Base3  = TCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAG

startCodons={}
codonEntries={}

f=open(codons)
aminoacids=f.readline().split()[2]
starts=f.readline().split()[2]
base1=f.readline().split()[2]
base2=f.readline().split()[2]
base3=f.readline().split()[2]
f.close()

i=0

while i<64:
	codon=base1[i]+base2[i]+base3[i]
	if starts[i]=="M":
		startCodons[codon]="M"
	codonEntries[codon]=aminoacids[i]
	i+=1

# psu|Lmjchr11    318346  G       K       2       2       35      13      .$.$....,,.,,TT ######EHC=#II   apidb|rna_LmjF11.0810-1 2580    +       CTG     CTT

keys={}

for line in open(pileup):
	tokens=line.split()
	key=tokens[0]+tokens[1]
	if key not in keys:
		keys[key]=0
	keys[key]+=1


for line in open(pileup):
	tokens=line.split()
	key=tokens[0]+tokens[1]

	wild=tokens[13-1].strip()
	observed=tokens[14-1].strip()
	aa1=codonEntries[wild]
	aa2=codonEntries[observed]
	print line.strip()+"\t"+aa1+"\t"+aa2
