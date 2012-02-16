#!/usr/bin/python

import sys

pileup=sys.argv[1]
codons=sys.argv[2]

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


for line in open(pileup):
	tokens=line.split()
	key=tokens[0]+tokens[1]

	wild=tokens[12].strip()
	observed=tokens[13].strip()

	if wild==observed:
		continue

	aa1=codonEntries[wild]
	aa2=codonEntries[observed]

	if aa1==aa2:
		continue

	print line.strip()+"\t"+aa1+"\t"+aa2
